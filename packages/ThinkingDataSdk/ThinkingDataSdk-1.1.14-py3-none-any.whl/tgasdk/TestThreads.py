import threading

import time

from tgasdk import LoggingConsumer, TGAnalytics
start = time.time()
tga = TGAnalytics(LoggingConsumer("F:/home/sdk/log",log_size=10))

def thread_func(tga,index):
    for i in range(100):
        common_prop = {
            "index":index,
            "si":i
        }
        tga.set_super_properties(common_prop)
        user_dict = {
            "char_id":i
        }
        tga.track(account_id="account_id",event_name="test",properties=user_dict)

    tga.clear_super_properties()
all_threads = []

for i in range(100):
    tt = threading.Thread(target=thread_func,args=(tga,i))
    tt.start()
    all_threads.append(tt)

try:
    print("wait for all threads ...")
except Exception as e:
    print("wait  ....")
for t in all_threads:
    t.join()

tga.close()
end = time.time()
print(end - start)
