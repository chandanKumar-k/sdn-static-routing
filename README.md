# sdn-static-routing
# Static Routing using SDN Controller (POX)

## 📌 Objective

To implement static routing in a Software Defined Network (SDN) using a controller-based approach and verify packet forwarding, flow rules, and network performance.

---

## 🛠️ Tools & Technologies Used

* Mininet (Network Emulator)
* POX Controller (OpenFlow 1.0)
* Open vSwitch (OVS)
* Ubuntu (VM)

---

## 🌐 Topology

### 🔹 Linear Topology (POX)

* 3 Hosts: h1, h2, h3
* 3 Switches: s1, s2, s3
* 1 Controller (POX)

Path:
h1 → s1 → s2 → s3 → h3

---

### 🔹 Firewall / Static Routing Topology (Ryu)

* h1 connected to s1
* h2 connected to s2
* h3 connected to s3
* s1 connected to s2 and s3

Special behavior:

* s2 is **blocked (no forwarding)**
* Traffic flows through **s1 → s3 only**

---

## ⚙️ How to Run the Project

### 🔹 Step 1: Start POX Controller

```bash
cd ~/pox
./pox.py log.level --DEBUG openflow.of_01 static_routing
```

---

### 🔹 Step 2: Start Mininet

```bash
sudo mn --topo linear,3 --mac --controller remote,ip=127.0.0.1,port=6633 --switch ovsk,protocols=OpenFlow10
```

---

### 🔹 Step 3: Test Connectivity

```bash
pingall
h1 ping h3
```

---

### 🔹 Step 4: Check Bandwidth

```bash
iperf
```

---

### 🔹 Step 5: View Flow Tables

```bash
dpctl dump-flows
```

---

## 📊 Results

### ✅ Ping Results

* 0% packet loss
* Successful communication between all hosts

### ✅ Latency Observation

* First packet delay higher due to:

  * ARP resolution
  * Flow rule installation
* Subsequent packets faster

### ✅ Throughput (iperf)

* ~15–17 Gbits/sec (virtual environment)

### ✅ Flow Table Verification

* Flow rules installed dynamically
* Match–Action mechanism working correctly

---

## 🧠 Key Concepts Used

* SDN Architecture (Control Plane & Data Plane)
* OpenFlow Protocol
* Match–Action Flow Rules
* PacketIn Event Handling
* Flow Rule Installation
* Static Routing using Controller

---

## 🔍 Working Explanation

1. Host sends packet
2. Switch does not know path
3. Packet sent to controller (PacketIn)
4. Controller installs flow rule
5. Switch forwards packets using flow table
6. Future packets bypass controller

---

## 📁 Files Included

* `static_routing.py` → POX Controller code
* `topology.py` → Custom Mininet topology

---

## 🎯 Conclusion

The project successfully demonstrates SDN-based static routing using POX and Ryu controllers.
Flow rules are dynamically installed, and network behavior is controlled centrally, ensuring efficient and flexible packet forwarding.

---

## 👨‍💻 Author

Chandan Kumar
