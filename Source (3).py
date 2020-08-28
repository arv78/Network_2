import random
import numpy as np

def walsh_table(size):
    curr_size = 2
    last_table = np.ones((1,1), dtype = int)
    if (size == 1):
        return last_table
    while (curr_size // 2  < size):
        w_table = np.ones((curr_size,curr_size), dtype = int)
        # three same parts
        for i in range(0,curr_size//2):
            for j in range(0,curr_size//2):
                w_table[i][j] = last_table[i][j]
        for i in range(0,curr_size//2):
            for j in range(curr_size//2,curr_size):
                w_table[i][j] = last_table[i][j-(curr_size//2)]
        for i in range(curr_size//2,curr_size):
            for j in range(0,curr_size//2):
                w_table[i][j] = last_table[i-(curr_size//2)][j]
        # reverse the last part
        for i in range(curr_size//2,curr_size):
            for j in range(curr_size//2,curr_size):
                w_table[i][j] = last_table[i-(curr_size//2)][j-(curr_size//2)] * -1
        # saving the last table
        last_table = w_table
        curr_size *= 2
    return w_table

def random_generation(length):
    data = []
    for i in range(length):
        data.append(random.randint(0,1))
    return data

def prob (probability):
    chance = random.randint(0,100)
    if (chance <= probability):
        return True
    else:
        return False

def TDMA(probability,A,B,C,D,channel,A_rate,B_rate,C_rate,D_rate):
    
    total_time_slot = len(A)//A_rate
    total_time_slot += len(B)//A_rate
    total_time_slot += len(C)//A_rate
    total_time_slot += len(D)//A_rate

    sent_data = len(A) + len(B) + len(C) +len(D)
    num_steps = 0
    while (A or B or C or D):
        num_steps += 1
        size = 0
        while (size <= len(channel)):
            flag = 0
            if (A and prob(probability)):
                flag = 1
                # print("here1")
                if (size + A_rate > len(channel)):
                    break
                if (len(A) < A_rate):
                    for i in range(len(A)):
                        channel[size+i] = A.pop(0)
                else:
                    for i in range(A_rate):
                        channel[size+i] = A.pop(0)
                size += A_rate
            if (B and prob(probability)):
                flag = 1
                # print("here2")
                if (size + B_rate > len(channel)):
                    break
                if (len(B) < B_rate):
                    for i in range(len(B)):
                        channel[size+i] = B.pop(0)
                else:
                    for i in range(B_rate):
                        channel[size+i] = B.pop(0)
                size += B_rate
            if (C and prob(probability)):
                flag = 1
                # print("here3")
                if (size + C_rate > len(channel)):
                    break
                if (len(C) < C_rate):
                    for i in range(len(C)):
                        channel[size+i] = C.pop(0)
                else:
                    for i in range(C_rate):
                        channel[size+i] = C.pop(0)
                size += C_rate
            if (D and prob(probability)):
                flag = 1
                # print("here4")
                if (size + D_rate > len(channel)):
                    break
                if (len(D) < D_rate):
                    size += len(D)
                    for i in range(len(D)):
                        channel[size+i] = D.pop(0)
                else:
                    for i in range(D_rate):
                        channel[size+i] = D.pop(0)
                    size += D_rate
            if (flag == 0):
                break
        #printing the channel and then unload the channel
        for j in range (len(channel)):
        #     print(channel[j])
            channel[j] = 0

        print(A)
        print(B)
        print(C)
        print(D)
        print("________________")
    total_rate = sent_data // total_time_slot
    print("TDMA rate: ",total_rate)
    print(num_steps)


def CDMA(probability,A,B,C,D,channel,A_rate,B_rate,C_rate,D_rate,num_users):
    num_of_receiver = eval(input("number of the receiver: "))
    # creating walsh table
    W_T = walsh_table(num_users)
    print("Walsh table:")
    print(W_T)
    curr_size_channel = 0
    receiver_list = []

    while (A or B or C or D):
        coded = []

        if (A):
            temp = A.pop(0)
            if (temp == 0):
                temp = -1
            for j in range(len(W_T)):
                coded.append(temp * W_T[0][j])
        # if the node is silent
        else:
            for j in range(len(W_T)):
                coded.append(0)
        if (B):
            temp = B.pop(0)
            if (temp == 0):
                temp = -1
            for j in range(len(W_T)):
                coded[j] += temp * W_T[1][j]
        # if the node is silent
        else:
            for j in range(len(W_T)):
                coded[j] += (0)
        if (C):
            temp = C.pop(0)
            if (temp == 0):
                temp = -1
            for j in range(len(W_T)):
                coded[j] += temp * W_T[2][j]
        # if the node is silent
        else:
            for j in range(len(W_T)):
                coded[j] += (0)
        if (D):
            temp = D.pop(0)
            if (temp == 0):
                temp = -1
            for j in range(len(W_T)):
                coded[j] += temp * W_T[3][j]
        # if the node is silent
        else:
            for j in range(len(W_T)):
                coded[j] += (0)
        # data go through the channel
        for k in range(len(coded)):
            channel[k+curr_size_channel] = coded[k]
        curr_size_channel += len(coded)
        # if channel was full send the data
        if (len(coded) + curr_size_channel > len(channel)):
            for l in range(0,len(channel) - (len(channel)%len(coded)),len(coded)):
                result = 0
                for i in range(len(W_T)):
                    result += W_T[num_of_receiver-1][i] * channel[l+i]
                # print(result)
                result = result // len(W_T)
                if (result == -1):
                    result = 0
                elif (result == 0):
                    result = -1
                # print(result)
                curr_size_channel = 0
                # adding the final result 
                receiver_list.append(result)
    return receiver_list


def dynamic_TDMA(probability,A,B,C,D,channel,A_rate,B_rate,C_rate,D_rate):
    num_time_slot_A = 1
    num_time_slot_B = 1
    num_time_slot_C = 1
    num_time_slot_D = 1
    num_time_slot_list = []
    num_time_slot_list.append(len(A)//A_rate)
    num_time_slot_list.append(len(B)//B_rate)
    num_time_slot_list.append(len(C)//C_rate)
    num_time_slot_list.append(len(D)//D_rate)

    sent_data = len(A) + len(B) + len(C) +len(D)

    # in this section first we want to make sure all the nodes have close number of time slots to some degree
    while (True):
        error = 0
        for i in range(3):
            for j in range(3,i,-1):
                if (abs(num_time_slot_list[i]-num_time_slot_list[j]) > error):
                    error = abs(num_time_slot_list[i]-num_time_slot_list[j])
        if (error <= 5):
            break
        max = 0
        max_index = -1
        for i in range(len(num_time_slot_list)):
            if (num_time_slot_list[i] > max):
                max = num_time_slot_list[i]
                max_index = i
        num_time_slot_list[max_index] = num_time_slot_list[max_index] // 2
        if (max_index == 0):
            num_time_slot_A += 1
        elif (max_index == 1):
            num_time_slot_B += 1
        elif (max_index == 2):
            num_time_slot_C += 1
        elif (max_index == 3):
            num_time_slot_D += 1
    
    total_time_slot = num_time_slot_list[0]
    total_time_slot += num_time_slot_list[1]
    total_time_slot += num_time_slot_list[2]
    total_time_slot += num_time_slot_list[3]

    print("number of time slots for node A is: ",num_time_slot_A)
    print("number of time slots for node B is: ",num_time_slot_B)
    print("number of time slots for node C is: ",num_time_slot_C)
    print("number of time slots for node D is: ",num_time_slot_D)

    num_steps = 0
    while (A or B or C or D):
        num_steps += 1
        size = 0
        while (size <= len(channel)):
            flag = 0
            for o in range(num_time_slot_A):
                if (A and prob(probability)):
                    flag = 1
                    # print("here1")
                    if (size + A_rate > len(channel)):
                        break
                    if (len(A) < A_rate):
                        for i in range(len(A)):
                            channel[size+i] = A.pop(0)
                    else:
                        for i in range(A_rate):
                            channel[size+i] = A.pop(0)
                    size += A_rate
            for o in range(num_time_slot_B):
                if (B and prob(probability)):
                    flag = 1
                    # print("here2")
                    if (size + B_rate > len(channel)):
                        break
                    if (len(B) < B_rate):
                        for i in range(len(B)):
                            channel[size+i] = B.pop(0)
                    else:
                        for i in range(B_rate):
                            channel[size+i] = B.pop(0)
                    size += B_rate
            for o in range(num_time_slot_C):
                if (C and prob(probability)):
                    flag = 1
                    # print("here3")
                    if (size + C_rate > len(channel)):
                        break
                    if (len(C) < C_rate):
                        for i in range(len(C)):
                            channel[size+i] = C.pop(0)
                    else:
                        for i in range(C_rate):
                            channel[size+i] = C.pop(0)
                    size += C_rate
            for o in range(num_time_slot_D):
                if (D and prob(probability)):
                    flag = 1
                    # print("here4")
                    if (size + D_rate > len(channel)):
                        break
                    if (len(D) < D_rate):
                        for i in range(len(D)):
                            channel[size+i] = D.pop(0)
                    else:
                        for i in range(D_rate):
                            channel[size+i] = D.pop(0)
                    size += D_rate
            if (flag == 0):
                break
        #printing the channel and then unload the channel
        for j in range (len(channel)):
        #     print(channel[j])
            channel[j] = 0

        print(A)
        print(B)
        print(C)
        print(D)
        print("________________")

    total_rate = sent_data // total_time_slot
    print("dynamic_TDMA rate: ",total_rate)
    print(num_steps)


def check_data_list(data_list):
    flag = 0
    for i in range(len(data_list)):
        if (len(data_list[i]) != 0):
            flag = 1
    if (flag == 1):
        return True
    elif (flag == 0):
        return False

def TDMA_B(probability,data_list,channel,A_rate,B_rate,C_rate,D_rate):
    sent_data = 0
    total_time_slot = 0
    for i in range(len(data_list)):
        sent_data += len(data_list[i])
        if (i < 100):
            rate = A_rate
        elif (i < 200):
            rate = B_rate
        elif (i < 300):
            rate = C_rate
        elif (i < 400):
            rate = D_rate
        total_time_slot += len(data_list[i])//rate

    last_j = 0
    last_flag = 0
    flag_2 = 0
    num_steps = 0
    while (check_data_list(data_list) or flag_2 == 0):
        num_steps += 1
        size = 0
        flag = last_flag    
        for j in range(last_j,len(data_list)):
            if (len(data_list[j]) != 0 and prob(probability)):
                flag = 1
                if (j < 100):
                    rate = A_rate
                elif (j < 200):
                    rate = B_rate
                elif (j < 300):
                    rate = C_rate
                elif (j < 400):
                    rate = D_rate

                if (size + rate > len(channel)):
                    last_j = j
                    last_flag = flag
                    break
                if (len(data_list[j]) < rate):
                    size += len(data_list[j])
                    for i in range(len(data_list[j])):
                        channel[size+i] = data_list[j].pop(0)
                else:
                    for i in range(rate):
                        channel[size+i] = data_list[j].pop(0)
                    size += rate
                # print(data_list[j])
            if (j == 399):
                last_flag = 0
                last_j = 0
        if (flag == 0):
            flag_2 = 1
        # unload the channel
        for j in range (len(channel)):
            channel[j] = 0
    for k in range (len(data_list)):
        print(data_list[k])
    print("________________")
    print ("\n")
    total_rate = sent_data // total_time_slot
    print("TDMA_B rate: ",total_rate)
    print(num_steps)

def CDMA_B(probability,data_list,channel,A_rate,B_rate,C_rate,D_rate,num_users):
    num_of_receiver = eval(input("number of the receiver: "))
    print("data: ")
    print(data_list[num_of_receiver-1])
    # creating walsh table
    W_T = walsh_table(num_users)
    print("Walsh table:")
    print(W_T)

    curr_size_channel = 0
    receiver_list = []
    receiver_list_2 = []

    while (check_data_list(data_list)):
        coded = []
        for i in range(len(W_T)):
            coded.append(0)
        for i in range(len(W_T)):
            if (len(data_list[i]) != 0):
                temp = data_list[i].pop(0)
                if (temp == 0):
                    temp = -1
                for j in range(len(W_T)):
                    coded[j] += temp * W_T[i][j]
        
        result_2 = 0
        for k in range(len(coded)):
            result_2 += coded[k] * W_T[num_of_receiver-1][k]
        result_2 = result_2 // len(W_T)
        if (result_2 == -1):
            result_2 = 0
        elif (result_2 == 0):
            result_2 = -1
        receiver_list_2.append(result_2)

        # data go through the channel
        result = 0
        for k in range(len(coded)):
            channel[curr_size_channel] = coded[k]
            curr_size_channel += 1
            # if channel is full
            if (curr_size_channel >= len(channel)):
                # print(k,curr_size_channel)
                # input("here")
                # print("channel: ")
                # for i in range (curr_size_channel):
                #     print(channel[i])
                # print("_____________")
                for i in range(curr_size_channel):
                    result += W_T[num_of_receiver-1][(k-(curr_size_channel-1)) + i] * channel[i]
                curr_size_channel = 0
            # at the last part of the list, there's a smaller part which remains
            elif (k >= len(coded) - (len(coded)%len(channel))):
                # print(k,curr_size_channel)
                # input("here")
                for i in range(k,len(coded)):
                    result += W_T[num_of_receiver-1][i] * channel[i-k]
                curr_size_channel = 0
        result = result // len(W_T)
        if (result == -1):
            result = 0
        elif (result == 0):
            result = -1

        # adding the final result
        receiver_list.append(result)
    return receiver_list_2

def dynamic_TDMA_B(probability,data_list,channel,A_rate,B_rate,C_rate,D_rate):
    sent_data = 0
    total_time_slot = 0
    for i in range(len(data_list)):
        sent_data += len(data_list[i])

    num_iterations = []
    num_time_slot_list = []
    for i in range (len(data_list)):
        num_iterations.append(1)
        if (i < 100):
            rate = A_rate
        elif (i < 200):
            rate = B_rate
        elif (i < 300):
            rate = C_rate
        elif (i < 400):
            rate = D_rate
        num_time_slot_list.append(len(data_list[i])//rate)

    # in this section first we want to make sure all the nodes have close number of time slots to some degree
    while (True):
        error = 0
        for i in range(399):
            for j in range(399,i,-1):
                if (abs(num_time_slot_list[i]-num_time_slot_list[j]) > error):
                    error = abs(num_time_slot_list[i]-num_time_slot_list[j])
        if (error <= 5):
            break
        
        # finding the max num_time_slots in the nodes
        max = 0
        max_index = -1
        for i in range(len(num_time_slot_list)):
            if (num_time_slot_list[i] > max):
                max = num_time_slot_list[i]
                max_index = i

        num_time_slot_list[max_index] = num_time_slot_list[max_index] // 2
        num_iterations[max_index] += 1
    
    for i in range (len(num_iterations)):
        print("number of time slots for node ",i," is: ",num_iterations[i])

    for i in range(len(num_time_slot_list)):
        total_time_slot += num_time_slot_list[i]

    input("continue?!")
    last_j = 0
    last_flag = 0
    flag_2 = 0
    num_steps = 0
    while (check_data_list(data_list) or flag_2 == 0):
        num_steps += 1
        size = 0
        flag = last_flag
        for j in range(last_j,len(data_list)):
            for o in range(num_iterations[j]):
                if (len(data_list[j]) > 0 and prob(probability)):
                    flag = 1
                    if (j < 100):
                        rate = A_rate
                    elif (j < 200):
                        rate = B_rate
                    elif (j < 300):
                        rate = C_rate
                    elif (j < 400):
                        rate = D_rate

                    if (size + rate > len(channel)):
                        last_j = j
                        last_flag = flag
                        break
                    if (len(data_list[j]) < rate):
                        size += len(data_list[j])
                        for i in range(len(data_list[j])):
                            channel[size+i] = data_list[j].pop(0)
                    else:
                        for i in range(rate):
                            channel[size+i] = data_list[j].pop(0)
                        size += rate
                # print(data_list[j])
            if (j == 399):
                last_flag = 0
                last_j = 0
        if (flag == 0):
            flag_2 = 1
        # unload the channel
        for j in range (len(channel)):
            channel[j] = 0
    for k in range (len(data_list)):
        print(data_list[k])
    print("________________")
    print ("\n")
    total_rate = sent_data // total_time_slot
    print("dynamic_TDMA_B rate: ",total_rate)
    print(num_steps)

def main():

    # part A
    A = [1,0,0,0,1,0,1,1,1,1,0,0,0,0,1,1,0,1,1,1,1,1,0,1,1,0,0,0,0,1,1,1,1,1,0,0,0,1,1,0,0,0,1,1,1,0,1,0,1,
    0,0,0,0,1,1,1,1,1,1,0,1,1,0,1,1,1,0,1,0,1,1,0,1,0,1,1,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,1,1,1,1,1,1,1,0,1,1,1,0,1,1,1,1,0,1,0]

    B = [1,1,1,0,1,1,0,1,1,1,0,1,1,0,1,0,1,1,1,1,1,1,0,0,0,0,1,1,1,1,1,1,1,1,0,0,1,1,0,1,0,1,1,1,1,1,1,0,1,
    1,1,0,1,1,1,1,1,1,0,1,1,1,0,1,1,1,1,0,1,1,1,1,0,1,1,1]

    C = [1,0,0,0,1,0,1,1,1,1,0,0,0,0,1,1,0,1,1,1,1,1,0,1,1,0,0,0,0,1,1,1,1,1,0,0,0,1,1,0,0,0,1,1,1,0,1,0,1,
    0,0,0,0,1,1,1,1,1,1,0,1,1,0,1,1,1,0,1,0,1,1,0,1,0,1,1,0,0,0,0,1,1,0,0,1,1,1,0,1,0,1,0,0,0]

    D = [0,0,0,1,0,0,1,0,0,0,0,1,1,1,1,1,1,0,1,1,1,0,1,0,1,0,0,0,0,1,0,0,1,0,1,1,1,1,0,1,0,1,0,0,0,0,1,1,0,
    0,0,1,1,0,1,0,0,1,0,0]

    channel = []
    for i in range(30):
        channel.append(0)

    # part B
    print("1- TDMA part A  2- CDMA part A  3- dynamic TDMA part A  4- TDMA part B  5- CDMA part B  6- dynamic TDMA part B ")
    choice = eval(input("select Algorithm:"))

    data_list = []
    for i in range(512):
        if (i < 100):
            data_list.append(random_generation(110))
        elif (i < 200):
            data_list.append(random_generation(75))
        elif (i < 300):
            data_list.append(random_generation(94))
        elif (i < 400):
            data_list.append(random_generation(60))
        elif (i < 512  and choice == 5):
            data_list.append([0])
        
    A_rate = 5
    B_rate = 3
    C_rate = 2
    D_rate = 4
    

    # part A
    if(choice == 1):
        TDMA(50,A,B,C,D,channel,A_rate,B_rate,C_rate,D_rate)
    if(choice == 2):
        receiver_list = CDMA(50,A,B,C,D,channel,A_rate,B_rate,C_rate,D_rate,4)
        print(receiver_list)
    if(choice == 3):
        dynamic_TDMA(50,A,B,C,D,channel,A_rate,B_rate,C_rate,D_rate)

    # part B
    if(choice == 4):
        TDMA_B(50,data_list,channel,A_rate,B_rate,C_rate,D_rate)
    if(choice == 5):
        receiver_list = CDMA_B(50,data_list,channel,A_rate,B_rate,C_rate,D_rate,400)
        print("data after decoding: ")
        print(receiver_list)
    if(choice == 6):
        dynamic_TDMA_B(50,data_list,channel,A_rate,B_rate,C_rate,D_rate)
main()