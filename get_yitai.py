import time
class RemoveUper:
    

    data_bytes=None
    data_bytes_list=[]
    index=0
    def start(self):
        for i in range(184):
            path="E:/学习/论文/else/初始数据/2020-12-29-14-13-10/2020-12-29-14-13-10-LS-{:0>6}.dat".format(i)
            with open(path,'rb') as f:
                lines=f.readlines()
            self.data_bytes=b''.join(lines)
            self.read_data()
        with open("E:/学习/论文/else/自己处理后的数据/temp.dat",'wb+') as f:
            f.writelines(self.data_bytes_list)
        return

    def read_data(self):
        self.index=0
        while self.index<len(self.data_bytes):
            if self.data_bytes[self.index:self.index+4]==b'\xeb\xeb\x90\x90':#上位机命令
                self.read_uper_command()
            self.index+=1
        return

    def read_uper_command(self):
        self.index+=4#跳过帧头
        #command=self.data_bytes[self.index:self.index+4]
        self.index+=4#跳过操作命令
        #total_section=self.data_bytes[self.index:self.index+2]
        #current_section=self.data_bytes[self.index+2:self.index+4]
        self.index+=4#跳过扇区长度
        data_length=self.data_bytes[self.index:self.index+4]
        data_length=int(data_length.hex(),16)
        self.index+=4#跳过数据长度
        self.data_bytes_list.append(self.data_bytes[self.index:self.index+data_length])
        self.index+=data_length#跳过数据
        return
class Get_Yitai:
    path="E:/学习/论文/else/自己处理后的数据/temp.dat"#"E:/学习/论文/else/（外协处理后）数字数据/2020-09-02-11-34-17-YC-0000000000.dat"
    data_bytes=None
    data_bytes_list=[]
    index=0
    def start(self):
        with open(self.path,'rb') as f:
            lines=f.readlines()
       
        self.data_bytes=b''.join(lines)
        data_length=len(self.data_bytes)
        self.read_data_frame(data_length)
        with open("E:/学习/论文/else/自己处理后的数据/2020-12-29-14-13-10-YC-000000.dat",'wb') as f:
            f.writelines(self.data_bytes_list)

        return

    def read_data_frame(self,data_length):
        index=self.index #这里用局部变量
        def read_frame(index):
            index+=4#跳过帧头
            if self.data_bytes[index:index+4]==b'\x00\x00\x00\x02':#太网数据帧结构
                #print("start index{}".format(index-4))
                self.data_bytes_list.append(self.data_bytes[index-4:index-4+1064])
                #print(self.data_bytes[index-4:index+1065].hex())
                index+=4#跳过帧类型
                time_tag=self.data_bytes[index:index+8].hex()
                index+=8#跳过时间标签
                data=self.data_bytes[index:index+20]
                while index<self.index+data_length:
                    if self.data_bytes[index:index+4]==b'\xfa\xfb\xfc\xfd':
                        #print("end index{}".format(index))
                        index+=1
                        break
                    else:
                        index+=1
                
            return index

        while index<self.index+data_length:
            if self.data_bytes[index:index+4]==b'\xea\xeb\xec\xed':
                index=read_frame(index)
                
            else:
                index+=1
        return


if __name__=='__main__':
    #r=RemoveUper()
    #r.start()
    g=Get_Yitai()
    g.start()

