from matplotlib import pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

class ClutterMap:
    path="E:/学习/论文/else/（外协处理后）数字数据/2020-09-02-11-34-17-YC-0000000000.dat"#"E:/学习/论文/else/自己处理后的数据/2020-12-29-14-13-10-YC-000000.dat"
    data_bytes=None
    index=0
    pic_index=0
    def start(self):
        with open(self.path,'rb') as f:
            lines=f.readlines()
       
        self.data_bytes=b''.join(lines)
        data_length=len(self.data_bytes)
        assert data_length/1064/6*10%10==0 ,"帧数不是6的整数倍"

        #for i in range(int(data_length/1064)):
            #print("{}...".format(self.data_bytes[i*1064:i*1064+40].hex()))
            #print(self.data_bytes[i*1064+1014:i*1064+1064].hex())
        print("有{}个数据帧，可以画{}张图".format(int(data_length/1064),int(data_length/1064/6)))
        for i in range(0,int(data_length/1064/6)):#int(data_length/1064/6)
            self.draw()

        return
    def draw(self):
        self.index+=1064*3#跳过前3帧，后3帧才是杂波
        port_dor=[]
        for i in range(4):
            port_dor.append([])
            for j in range(128):
                shift=self.index+36+256*i+2*j
                the_hex=self.data_bytes[shift:shift+2]
                port_dor[i].append(int.from_bytes(the_hex, byteorder='little', signed=False))
        self.index+=1064
        for i in range(4,8):
            port_dor.append([])
            for j in range(128):
                shift=self.index+36+256*(i-4)+2*j
                the_hex=self.data_bytes[shift:shift+2]
                port_dor[i].append(int.from_bytes(the_hex, byteorder='little', signed=False))
        self.index+=1064
        for i in range(8,12):
            port_dor.append([])
            for j in range(128):
                shift=self.index+36+256*(i-8)+2*j
                the_hex=self.data_bytes[shift:shift+2]
                port_dor[i].append(int.from_bytes(the_hex, byteorder='little', signed=False))
        self.index+=1064

        #self.index+=1064*3#跳过后3帧

        #开始画图
        ax=plt.gca()
        ax.xaxis.set_major_locator(plt.MultipleLocator(1))
        ax.yaxis.set_major_locator(plt.MultipleLocator(20))
        

        def reshape_data(data):
            x=[]
            y=[]
            z=[]
            for i in range(12):
                for j in range(128):
                    x.append(i)
                    y.append(j)
                    z.append(data[i][j])
            return np.array(x),np.array(y),np.array(z)
        
        fig = plt.figure(figsize=(12,8))
        ax = Axes3D(fig)
        ax.set_zlim3d([0,1300])
        ax.set_xlim([0,12])
        ax.set_ylim([0,140])
        x,y,z=reshape_data(port_dor)
        ax.get_proj = lambda: np.dot(Axes3D.get_proj(ax), np.diag([0.5, 1, 0.7, 0.7]))
        ax.plot_trisurf(x, y, z)
        ax.view_init(33,-26)
        #plt.show()
        self.pic_index+=1
        pic_path="E:/学习/论文/else/自己处理后的数据/杂波图/外协/杂波图{:0>6}.png".format(self.pic_index)
        plt.savefig(pic_path)
        plt.clf()
        plt.close()
        return




if __name__=='__main__':
    c=ClutterMap()
    c.start()


