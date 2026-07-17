### gp2, gp3 volumes:

Both **_gp2_**, **_gp3_** are general purpose volumes

However **_gp3_** is the new storage volume type in EBS

#### Advantages of using gp3 over gp2:

- 20% cheaper than the **_gp2_**
- Comes with baseline of 3000 IOPS, 125 Mib/s throughput
- IOPS, throughput are scaled independently of the storage size(unlike gp2 which provides around 3 IOPS per Gib of storage provisioned)
- Here baseline means without any burst/provisioning, one will get guaranteed, predictable performance

#### IOPS vs throughput:

- _IOPS_ normally means the number of input-output operations per second
  - Ex: 10k customers adding Apple Iphone into their cart during Amazon prime day sale event(small I/O ops into DB)
- _Throughput_ means per operation how much data can you send/receive
  - Ex: Argentina vs Spain FIFA final can be good example of high throughput where huge amount of data will be streamed into CDNs which in turn render that content to the local routers
