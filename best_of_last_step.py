import pandas as pd
from random import randint as randi
import random
from pathlib import Path

from AgentWrapper import AgentAbstract

class bestOfLastStep(AgentAbstract):

    def __new__(self, target):
        Common_Data = AgentAbstract.Common_Data
        if Common_Data.io_type != 'Z':
            raise Exception("I work only with Z datatype!")
        if Common_Data.io_topo == 'distinct':
            return bestOfLastStep_Z_distinct(target)
        elif Common_Data.io_topo == 'ring':
            return bestOfLastStep_Z_ring(target)



class bestOfLastStep_Z_distinct(AgentAbstract):

    def __init__(self, target):
        self.target = target
        self.freq_chart = pd.DataFrame(columns = ['prior_mem', 'my_output', 'system_returns', 'norm', 'freq'])
        self.incoming_log = []
        self.output_log = []
        self.sim_no = 0

    def process(self, incoming_values, round_no):
        incoming_vals_in_tup = tuple(incoming_values)

        # Save data in last round.
        if round_no == AgentAbstract.Common_Data.total_rounds_count-1:
            folder_add = Path((str(id(AgentAbstract))+"_"+str(self.sim_no)))
            self.sim_no += 1
            folder_add.mkdir(parents=True, exist_ok=True)
            self.freq_chart.to_csv(folder_add / Path(str(id(self))+'_freqChart.csv'))
            with open(folder_add / Path(str(id(self))+'_log.txt'), 'w') as f:
                for ic,ou in zip(self.incoming_log, self.output_log):
                    f.write(f"Incoming value: {ic}; Output: {ou}\n")
        self.incoming_log.append(incoming_vals_in_tup)

        # Not enough data to calculate past_mem_hash so through garbage in network.
        if round_no < 2:
            self.num_incoming_nodes = len(incoming_values)
            self.output_log.append(self.target)
            return self.target
        else:
            # Log the outcome corresponding to your last value sent into network.
            df = self.freq_chart
            past_mem_hash = self.calc_past_mem_hash()
            curr_mem_hash = self.calc_curr_mem_hash()
            df_slice = df.loc[  (df['prior_mem'] == past_mem_hash) &
                                (df['my_output'] == self.output_log[-1]) &
                                (df['system_returns'] == incoming_vals_in_tup)]
            if df_slice.empty:
                # If this sequence of events has happened for first time.
                incoming_diff = AgentAbstract.get_diff(AgentAbstract, self.target, incoming_values)
                incoming_score = AgentAbstract.get_norm(AgentAbstract, incoming_diff)
                df.loc[len(df.index)] = [past_mem_hash, self.output_log[-1], incoming_vals_in_tup, incoming_score, 1]
            else:
                # If this sequence of events has already occurred.
                assert len(df_slice.index) == 1
                df.loc[df_slice.index[0], 'freq'] += 1
            if AgentAbstract.Common_Data.is_training:
                # If this is a training round
                best_poss_output = randi(AgentAbstract.Common_Data.io_min, AgentAbstract.Common_Data.io_max)
            else:
                # If this is a evaluation round
                best_poss_output = self.best_output(curr_mem_hash)
            self.output_log.append(best_poss_output)
            return best_poss_output

    def calc_past_mem_hash(self):
        return self.incoming_log[-2]

    def calc_curr_mem_hash(self):
        return self.incoming_log[-1]

    def best_output(self, curr_mem_hash):
        df = self.freq_chart
        df_slice = df[df.prior_mem == curr_mem_hash]
        if df_slice.empty:
            df_slice = df[df.norm == df.norm.min()]
            rand_ind_out_of_min = randi(0,len(df_slice)-1)
            return df_slice.loc[df_slice.index[rand_ind_out_of_min]]['my_output']
        else:
            df_slice = df_slice[df_slice.norm == df_slice.norm.min()]
            rand_ind_out_of_min = randi(0, len(df_slice) - 1)
            return df_slice.loc[df_slice.index[rand_ind_out_of_min]]['my_output']

    def new_target(self, new_target):
        self.target = new_target


class bestOfLastStep_Z_ring(AgentAbstract):

    def __init__(self, target):
        self.target = target
        self.freq_chart = pd.DataFrame(columns = ['prior_mem', 'my_output', 'system_returns', 'norm', 'freq'])
        self.incoming_log = []
        self.output_log = []
        self.sim_no = 0

    def process(self, incoming_values, round_no):
        # Put your implementation here.
        pass