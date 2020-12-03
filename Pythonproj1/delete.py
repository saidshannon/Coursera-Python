import numpy as np
from PIL import Image
from IPython.display import display
a=np.linspace(0,10,5)
#print(a)
b=np.arange(0,10,2)
#print(b)
c=np.random.rand(1,1)
#print(c)
d=np.random.rand(2,2)
#print(d.shape)
e=np.random.rand(10)
#print(e.reshape(5,2))
k=np.reshape(e,(5,2))
print(k)
f=np.random.rand(4,4)
#print(f.dtype.name)
g=np.full(f.shape,10)
#print(g)
h=np.random.rand(4)
print(h.ndim)
i=np.array([[1,2,3,4]])
print(i.ndim)

#image array
im=Image.open("Testimg.tiff")
display(im)
array=np.array(im)
#print(array)
mask=np.full(array.shape,255)
marray=array-mask
#print(marray)
marray=marray*(-1)
moarray=marray.reshape(100,400)

#print(marray)
display(Image.fromarray(moarray))





