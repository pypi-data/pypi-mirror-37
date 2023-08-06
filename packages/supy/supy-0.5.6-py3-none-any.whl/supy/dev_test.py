
# var_list_x = [np.array(sd.output_name_n(i))
#               # for i in np.arange(size_var_list) + 1]
#               for i in np.arange(20)]
# sd.output_name_n(191)

from supy import sd
import numpy as np

size_var_list = sd.output_size()
for i in np.arange(size_var_list):
    print(sd.output_name_n(i))
