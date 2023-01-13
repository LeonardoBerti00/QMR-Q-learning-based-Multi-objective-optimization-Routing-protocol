from src.entities.uav_entities import DataPacket, FeedbackPacket, ACKPacket, HelloPacket, Packet
from src.utilities import utilities as util
from src.utilities import config

from scipy.stats import norm
import abc
import numpy as np
import math
class BASE_routing(metaclass=abc.ABCMeta):

    def __init__(self, drone, simulator):
        """ The drone that is doing routing and simulator object. """

        self.drone = drone
        self.simulator = simulator

        if self.simulator.communication_error_type == config.ChannelError.GAUSSIAN:
            self.buckets_probability = self.__init_guassian()

        self.current_n_transmission = 0
        self.hello_messages = {}  # { drone_id : most recent hello packet}
        self.network_disp = simulator.network_dispatcher
        self.simulator = simulator
        self.no_transmission = False
        self.opt_neighbors = []
        self.old_neighbors = []

    @abc.abstractmethod
    def relay_selection(self, geo_neighbors, packet):
        pass

    def routing_close(self):
        self.no_transmission = False

    def drone_reception(self, src_drone, packet: Packet, current_ts):

        if isinstance(packet, HelloPacket):
            src_id = packet.src_drone.identifier
            self.hello_messages[src_id] = packet  # add packet to our dictionary
            self.updateNeighborTable(packet)

        elif isinstance(packet, DataPacket):
            self.no_transmission = True
            self.drone.accept_packets(packet, src_drone, current_ts)

            # build ack for the reception
            self.drone.received_pck[packet.event_ref] = (current_ts, src_drone)
            maxx = -121341
            for i in range(self.simulator.n_drones + 1):
                if (self.drone.neighbor_table[i, 9] > maxx):
                    maxx = self.drone.neighbor_table[i, 9]

            ack_packet = ACKPacket(self.drone, src_drone, self.simulator, packet, maxx, current_ts)
            self.drone.sended_ack[ack_packet.event_ref] = (current_ts, src_drone)
            self.unicast_message(ack_packet, self.drone, src_drone, current_ts)

        elif isinstance(packet, ACKPacket):
            self.drone.remove_packets([packet.acked_packet])
            self.drone.received_pck[packet.event_ref] = (current_ts, src_drone)

            #Update the MAC delay
            tm = packet.time_step_creation - current_ts
            if (len(self.drone.delays[packet.dst_drone.identifier]) < 50):
                n = len(self.drone.delays[packet.dst_drone.identifier])
            elif (len(self.drone.delays[packet.dst_drone.identifier]) >= 50):
                n = 50
            sum = 0
            for i in range(n):
                sum += self.drone.delays[packet.dst_drone.identifier][-i]
            if (n == 0):
                mac = tm
            else:
                mac = ((1 - self.simulator.beta) * sum / n) + (self.simulator.beta * tm)
            self.drone.delays[packet.dst_drone.identifier].append(mac)
            self.drone.neighbor_table[packet.dst_drone.identifier, 11] = mac

            if self.drone.buffer_length() == 0:
                self.current_n_transmission = 0
                self.drone.move_routing = False

            self.drone.routing_algorithm.feedback(0, packet.src_drone.identifier, packet.best_action)


    def drone_identification(self, drones, cur_step):
        """ handle drone hello messages to identify neighbors """
        # if self.drone in drones: drones.remove(self.drone)  # do not send hello to yourself
        if cur_step % config.HELLO_DELAY != 0:  # still not time to communicate
            return

        sended_ack = [0 for drone in range(self.simulator.n_drones)]
        for key in self.drone.sended_ack:
            if self.drone.sended_ack[key][0] > self.simulator.cur_step - 500:
                sended_ack[self.drone.sended_ack[key][1].identifier] += 1

        received_pck = [0 for drone in range(self.simulator.n_drones)]
        for key in self.drone.received_pck:
            if (self.drone.received_pck[key][0] > self.simulator.cur_step - 500):
                received_pck[self.drone.received_pck[key][1].identifier] += 1

        my_hello = HelloPacket(self.drone, self.drone.coords, self.drone.residual_energy, self.drone.speed,
                               self.drone.next_target(), self.drone.queuing_delay, self.drone.discount_factor, received_pck, sended_ack)

        self.broadcast_message(my_hello, self.drone, drones, cur_step)


    def routing(self, depot, drones, cur_step):
        # set up this routing pass

        self.drone_identification(drones, cur_step)    #ogni 5 time step

        self.send_packets(cur_step)                #ogni 10 time step

        # close this routing pass
        self.routing_close()


    def send_packets(self, cur_step):

        # FLOW 0
        if self.no_transmission or self.drone.buffer_length() == 0:
            return

        # if the drone is near to the depot, deliver the packets
        if util.euclidean_distance(self.simulator.depot.coords, self.drone.coords) <= self.simulator.depot_com_range:
            # add error in case
            self.transfer_to_depot(self.drone.depot, cur_step)

            self.drone.move_routing = False
            self.current_n_transmission = 0
            return

        #ogni 10 time step entriamo qua
        if cur_step % self.simulator.drone_retransmission_delta == 0:
            self.old_neighbors = self.opt_neighbors
            self.opt_neighbors = []
            for hpk_id in self.hello_messages:
                hpk: HelloPacket = self.hello_messages[hpk_id]

            for i in range(self.simulator.n_drones):
                arrival_time = self.drone.neighbor_table[i, 6]
                #se l'informazione non è troppo vecchia lo consideriamo come neighbor
                if (self.simulator.cur_step - arrival_time < self.simulator.ExpireTime and arrival_time != 0):
                    self.opt_neighbors.append(self.simulator.drones[i])                     #chiedere se si può fare questa cosa

            self.updateDiscountFactor()

            # send packets
            for pkd in self.drone.all_packets():
                
                self.simulator.metrics.mean_numbers_of_possible_relays.append(len(self.opt_neighbors))

                best_neighbor = self.relay_selection(self.opt_neighbors, pkd)  # compute score

                #if we encounter a routing hole problem
                if isinstance(best_neighbor, str):
                    src = None
                    for i in range(len(self.drone.buffer)):
                        if (self.drone.buffer[i][0] == pkd[0]):
                            src = self.drone.buffer[i][1]

                    if (src is None):
                        raise Exception("src drone is None")

                    #calculating the max Q-value
                    maxx = -121341
                    for i in range(self.simulator.n_drones + 1):
                        if (self.drone.neighbor_table[i, 9] > maxx):
                            maxx = self.drone.neighbor_table[i, 9]

                    feedback = FeedbackPacket(self.drone, src.identifier, self.simulator, maxx, self.simulator.cur_step)
                    self.unicast_message(feedback, self.drone, src, cur_step)


                elif best_neighbor is not None:
                    self.unicast_message(pkd[0], self.drone, best_neighbor, cur_step)

                    self.current_n_transmission += 1

                    self.drone.sended_pck[pkd[0].event_ref] = (cur_step, best_neighbor)

                    for i in range(len(self.drone.buffer)):
                        if (self.drone.buffer[i][0] == pkd[0]):
                            arr_time = self.drone.buffer[i][2]

                    last_queuing_delay = cur_step - arr_time
                    self.drone.queuing_delays.append(last_queuing_delay)
                    op1 = (1 - self.simulator.beta) * (sum(self.drone.queuing_delays) / len(self.drone.queuing_delays))
                    op2 = (self.simulator.beta * last_queuing_delay)
                    self.drone.queuing_delay = op1 + op2


    def updateNeighborTable(self, hpk):
        drone_id = hpk.src_drone.identifier
        self.drone.neighbor_table[drone_id, 0] = hpk.cur_pos[0]
        self.drone.neighbor_table[drone_id, 1] = hpk.cur_pos[1]
        self.drone.neighbor_table[drone_id, 2] = hpk.res_nrg
        self.drone.neighbor_table[drone_id, 3] = hpk.speed
        self.drone.neighbor_table[drone_id, 4] = hpk.next_target[0]
        self.drone.neighbor_table[drone_id, 5] = hpk.next_target[1]
        self.drone.neighbor_table[drone_id, 6] = self.simulator.cur_step
        self.drone.neighbor_table[drone_id, 7] = hpk.dis_fac
        self.drone.neighbor_table[drone_id, 8] = hpk.delay
        actual_delay = hpk.delay + self.drone.neighbor_table[drone_id, 11]
        self.drone.actual_delays.append(actual_delay)
        std = np.std(np.array(self.drone.actual_delays))
        if (std > 0):
            e = abs(actual_delay - np.mean(np.array(self.drone.actual_delays))) / std
        else:
            e = actual_delay
        self.drone.neighbor_table[drone_id, 10] = 1 - math.exp(-e)

        #now we compute the link quality
        cont = 0
        flag1 = False
        flag2 = False

        for key in self.drone.sended_pck:
            if (self.drone.sended_pck[key][1].identifier == drone_id and self.drone.sended_pck[key][0] > self.simulator.cur_step - 500):
                cont += 1
        if (cont != 0):
            df = hpk.received_pck[self.drone.identifier] / cont
            flag1 = True

        cont = 0
        for key in self.drone.received_ack:
            if (self.drone.received_ack[key][1].identifier == drone_id and self.drone.received_ack[key][0] > self.simulator.cur_step - 500):
                cont += 1
        if (hpk.sended_ack[self.drone.identifier] != 0):
            dr = cont / hpk.sended_ack[self.drone.identifier]
            flag2 = True

        if (flag2 and flag1):
            self.drone.neighbor_table[drone_id, 12] = df * dr


    def updateDiscountFactor(self):
        unione = len(set(self.old_neighbors).union(set(self.opt_neighbors)))
        int = len(set(self.old_neighbors).intersection(set(self.opt_neighbors)))
        if (unione != 0):
            self.drone.discount_factor = 1 - ((unione - int) / unione)
        else:
            self.drone.discount_factor = 0


    def geo_neighborhood(self, drones, no_error=False):
        """
        @param drones:
        @param no_error:
        @return: A list all the Drones that are in self.drone neighbourhood (no matter the distance to depot),
            in all direction in its transmission range, paired with their distance from self.drone
        """

        closest_drones = []  # list of this drone's neighbours and their distance from self.drone: (drone, distance)

        for other_drone in drones:

            if self.drone.identifier != other_drone.identifier:  # not the same drone
                drones_distance = util.euclidean_distance(self.drone.coords,
                                                          other_drone.coords)  # distance between two drones

                if drones_distance <= min(self.drone.communication_range,
                                          other_drone.communication_range):  # one feels the other & vv

                    # CHANNEL UNPREDICTABILITY
                    if self.channel_success(drones_distance, no_error=no_error):
                        closest_drones.append((other_drone, drones_distance))

        return closest_drones

    def channel_success(self, drones_distance, no_error=False):
        """
        Precondition: two drones are close enough to communicate. Return true if the communication
        goes through, false otherwise.
        """

        assert (drones_distance <= self.drone.communication_range)

        if no_error:
            return True

        if self.simulator.communication_error_type == config.ChannelError.NO_ERROR:
            return True

        elif self.simulator.communication_error_type == config.ChannelError.UNIFORM:
            return self.simulator.rnd_routing.rand() <= self.simulator.drone_communication_success

        elif self.simulator.communication_error_type == config.ChannelError.GAUSSIAN:
            return self.simulator.rnd_routing.rand() <= self.gaussian_success_handler(drones_distance)

    def broadcast_message(self, packet, src_drone, dst_drones, curr_step):
        """ send a message to my neigh drones"""
        for d_drone in dst_drones:
            self.unicast_message(packet, src_drone, d_drone, curr_step)

    def unicast_message(self, packet, src_drone, dst_drone, curr_step):
        """ send a message to my neigh drones"""
        # Broadcast using Network dispatcher
        self.simulator.network_dispatcher.send_packet_to_medium(packet, src_drone, dst_drone,
                                                                curr_step + config.LIL_DELTA)
        if isinstance(packet, DataPacket):
            self.drone.sended_pck[packet.event_ref] = (curr_step, dst_drone)
        elif isinstance(packet, ACKPacket):
            self.drone.sended_ack[packet.event_ref] = (curr_step, dst_drone)

    def gaussian_success_handler(self, drones_distance):
        """ get the probability of the drone bucket """
        bucket_id = int(drones_distance / self.radius_corona) * self.radius_corona
        return self.buckets_probability[bucket_id] * config.GUASSIAN_SCALE

    def transfer_to_depot(self, depot, cur_step):
        """ self.drone is close enough to depot and offloads its buffer to it, restarting the monitoring
                mission from where it left it
        """
        depot.transfer_notified_packets(self.drone, cur_step)
        self.drone.empty_buffer()
        self.drone.move_routing = False

    # --- PRIVATE ---
    def __init_guassian(self, mu=0, sigma_wrt_range=1.15, bucket_width_wrt_range=.5):

        # bucket width is 0.5 times the communication radius by default
        self.radius_corona = int(self.drone.communication_range * bucket_width_wrt_range)

        # sigma is 1.15 times the communication radius by default
        sigma = self.drone.communication_range * sigma_wrt_range

        max_prob = norm.cdf(mu + self.radius_corona, loc=mu, scale=sigma) - norm.cdf(0, loc=mu, scale=sigma)

        # maps a bucket starter to its probability of gaussian success
        buckets_probability = {}
        for bk in range(0, self.drone.communication_range, self.radius_corona):
            prob_leq = norm.cdf(bk, loc=mu, scale=sigma)
            prob_leq_plus = norm.cdf(bk + self.radius_corona, loc=mu, scale=sigma)
            prob = (prob_leq_plus - prob_leq) / max_prob
            buckets_probability[bk] = prob

        return buckets_probability
