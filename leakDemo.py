from pymodelica import compile_fmu
from pyfmi import load_fmu
from matplotlib.pyplot import *
from numpy import *

fmu_name = compile_fmu('Pipeline','Pipeline.mo',version='2.0',target='me+cs')
# fmu_name = 'Pipeline.fmu'
pipeline = load_fmu(fmu_name)
pipeline.set('g',9.782757)
opts = pipeline.simulate_options()
opts['ncp'] = 3000
opts['solver'] = 'CVode'
opts['CVode_options']['rtol'] = 1e-6
t = linspace(0,300,3001)
Hin = 5.70868433*ones(t.size)
Hout = 1.99976362*ones(t.size)
l1 = zeros(t.size)
l2 = zeros(t.size)
l3 = 1.25e-4*(t>100)*(t<200)
l4 = zeros(t.size)
u = transpose(vstack((t,l1,l2,l3,l4)))
input_data = (['lambda[1]','lambda[2]','lambda[3]','lambda[4]'], u)
res = pipeline.simulate(final_time=300,options=opts,input=input_data)
Q1 = res['Q[1]']
Q5 = res['Q[5]']
t = res['time']
sigma = pipeline.get('sigma')[0]
r1 = sigma*random.randn(Q1.size)
r5 = sigma*random.randn(Q5.size)
plot(t,Q1+r1,t,Q5+r5)
grid(True)
legend(['$Q_1(t)$','$Q_5(t)$'],loc='best')
xlabel('Time (s)')
ylabel('Flow rate (m$^3$/s)')
show()