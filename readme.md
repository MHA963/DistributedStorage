# Distributed Storage Systems

This repository contains practical laboratory exercises, prototypes, and implementations developed for the **Distributed Storage Systems** course at Aarhus University.

---

## Course Overview

Distributed storage systems address the challenge of storing data persistently and reliably at scale across inherently unreliable hardware and servers. This repository covers the implementation of core network communications, distributed file systems, redundancy and erasure coding algorithms, and object storage interfaces.

### Key Concepts Covered

* **Network & RPC Protocols:** Raw TCP/UDP Sockets, JSON-RPC, REST APIs, and ZeroMQ.
* **Serialization & Formats:** Protocol Buffers and custom binary framing.
* **Distributed File & Block Systems:** NFS, AFS, HDFS, NAS, and SAN.
* **Reliability & Redundancy:** RAID architectures, Reed-Solomon Erasure Coding, and Random Linear Network Coding (RLNC).
* **Storage Optimization:** Data deduplication, delta encoding, and data compression.
* **Cloud & Modern Architectures:** Object Storage (S3 API, OpenStack Swift), Fog Storage, and Storage for AI/ML.

---

## Environment Setup & Prerequisites

* **Python:** Version 3.6 or newer (Python 3.11+ recommended)
* **Environment Manager:** Anaconda / Conda or `venv`

### 1. Create and Activate Virtual Environment

```bash
# Using Conda
conda create -n dist-storage python=3.11
conda activate dist-storage

# OR using standard venv
python3 -m venv env
source ./env/bin/activate      # Linux/macOS
./env/Scripts/activate.bat    # Windows
```

### 2. Install Required Python Packages

```bash
pip install gevent requests tinyrpc Flask protobuf pyzmq boto3 apscheduler
pip install git+http://git@github.com/steinwurf/pyerasure
```

*(PyErasure uses a research license for non-commercial educational use).*

### 3. External Tool Dependencies

* **Protocol Buffers Compiler (`protoc`):** Download `v24.1` or newer and add `bin/protoc` to your system `PATH`.
* **SQLite3:** Lightweight relational database.
* **Postman:** For inspecting and testing REST API endpoints.

---

## Weekly Syllabus & Lab Exercises

| Week | Lecture Topic | Lab Content & Prototypes |
| --- | --- | --- |
| **Week 1** | Networking Basics & Sockets | **Lab 1:** TCP Client-Server, Message Framing & File Uploads |
| **Week 2** | RPC, NFS, JSON-RPC, REST | **Lab 2:** JSON-RPC with `tinyrpc`, REST API with Flask |
| **Week 3** | AFS & Reliable Storage Foundations | **Lab 3:** Messaging with ZeroMQ & Protocol Buffers |
| **Week 4** | Hard Drives & RAID Levels | **Lab 4:** RAID Implementation over ZeroMQ |
| **Week 5** | Finite Fields & Reed-Solomon Codes | **Lab 5:** `pyerasure` & Reed-Solomon (RS) Coding |
| **Week 6** | Repair Problem & Regenerating Codes | **Lab 6:** Distributed Storage Prototype using RS Codes |
| **Week 7** | Regenerating Codes & XORBAS | **Lab 7:** Lost Fragment Regeneration with RS |
| **Week 8** | *Autumn Break* | — |
| **Week 9** | Hadoop Architecture | **Lab 8:** RLNC & Data Recovery using Recode |
| **Week 10** | Storage Virtualization, NAS & SAN | **Lab 9:** Mini Project Kickoff & Basic HDFS Pipeline |
| **Week 11** | Object Storage | **Lab 10:** AWS S3 Compatible Storage API |
| **Week 12** | Compression & Delta Encoding | Mini Project Implementation & Consultation |
| **Week 13** | Data Deduplication | **Lab 11:** Content-Defined Deduplication & Compression |
| **Week 14** | Fog Storage Systems | Mini Project Implementation & Consultation |
| **Week 15** | Storage Systems for AI/ML | Mini Project Finalization |

---

## Repository Structure

```text
.
├── labs/
│   ├── lab01_sockets/        # Raw socket communication & streaming file transfer
│   ├── lab02_rpc_rest/       # Flask REST APIs and JSON-RPC
│   ├── lab03_zmq_protobuf/   # ZeroMQ messaging & Protobuf serialization
│   ├── lab04_raid_zmq/       # Software RAID prototype over ZeroMQ
│   ├── lab05_reed_solomon/   # PyErasure setup and RS encoding/decoding
│   ├── lab06_distributed_rs/ # Simple multi-node storage with RS codes
│   ├── lab07_regeneration/   # Fragment regeneration and repair
│   ├── lab08_rlnc/           # Random Linear Network Coding
│   ├── lab09_hdfs/           # NameNode & DataNode pipeline
│   ├── lab10_s3_api/         # Object storage endpoints
│   └── lab11_dedup_compress/ # Compression & block-level deduplication
├── project/                  # Distributed Storage Mini-Project
└── README.md
```

---

## Evaluation & Exam

* **Course Format:** Weekly 2-hour lecture followed by 2-hour hands-on system implementation lab.
* **Assessment:** Individual 20-minute oral examination evaluated on course lecture slides and a written prototype report covering the systems implemented in the labs.