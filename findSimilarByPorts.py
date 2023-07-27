import pandas as pd


# 读取Excel文件
df = pd.read_excel('input/logNyuDorm0-300_Groupby(IP).xlsx')

# 以port为key，ip为value
ports_devices_list = {}

# 以ip为key，port为value
device_info_list = {}

# 遍历每一行数据
for index, row in df.iterrows():
    ip = row['ip']
    ports = row['port'].split(',')

    # 将端口列表按照升序排序。由于原来是字符串，要先转成int再转回字符串
    int_ports = [int(element) for element in ports]
    sorted_int_ports = sorted(int_ports)
    sorted_ports = [str(element) for element in sorted_int_ports]
    
    device_info_list[ip] = sorted_ports
    
    # 将排序后的端口列表转换为字符串作为字典的键
    key = ','.join(sorted_ports)
    
    # 检查是否已经存在该端口组合的设备 
    if key in ports_devices_list:
        # 如果已经存在，将当前设备IP添加到已有的列表中
        ports_devices_list[key].append(ip)
    else:
        # 如果不存在，创建一个新的列表，并将当前设备IP加入
        ports_devices_list[key] = [ip]

"""
for item in device_info_list:
    print(item)
"""

print("################# Same Ports Devices:")

for ports, devices in ports_devices_list.items():
    if len(devices) > 2:
        print(f"Same devices on these ports: {ports}")
        for device in devices:
            print(device)
        print('---')

df = pd.DataFrame(ports_devices_list.items(), columns=['ports', 'ips']) 
df['ips'] = df['ips'].apply(lambda x: ';'.join(x))
df.to_excel("same_ports_devices.xlsx", index=False)

print("################# Similar Ports Devices:")

def isWeakSimilar(portsA, portsB, bar_value=6):
    #这里传进来的portsA, portsB是字符串，要转化回列表
    portsA = portsA.split(",")
    portsB = portsB.split(",")

    if (abs(len(portsA) - len(portsB))) > (max(len(portsA), len(portsB)) / bar_value):
        return False
    
    common_ports = set(portsA) & set(portsB)
    if (max(len(portsA), len(portsB)) - len(common_ports)) > (max(len(portsA), len(portsB)) / bar_value):
        return False
    
    return True

similar_group_list = []

for ports, devices in ports_devices_list.items():
    
    similar_group = [(ports, devices)]

    for other_ports, other_devices in ports_devices_list.items():
        if other_ports != ports:
            if isWeakSimilar(ports, other_ports):
                similar_group.append((other_ports, other_devices))

    similar_group = sorted(similar_group) # 有的可能只是内部元素(元组)顺序不一样

    if similar_group not in similar_group_list: #前者是元组列表，后者是元组列表的列表
        similar_group_list.append(similar_group)


""""""
for group in similar_group_list:
    
    print("-------------")
    print("Devices in ports gourp:")

    for ports, devices in group:
        print(f"{ports}:{devices}")

print(len(similar_group_list))
