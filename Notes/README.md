**Replication**

**Leader election**
1. Two servers play “master” and “slave” roles.
Clients send operations (both READ and WRITE) to Leader.
Leader forwards WRiTE operations to one or more followers.
Finally, leader replies to client.

**Challenges**
Non-deterministic operations.  
No network partition—if leader cannot reach to followers, then the data will be inconsistent.  
State transfer between leader and followers.  
How to bring up a new follower after existing follower becomes leader.  

**Quorum concensus algorithm**
A distributed system is a set of processes working together to form a complete system.
Sometimes, it’s important that some processes agree on a result or a change of state before it’s actually reflected by the system.
Quorum represents the number of participants required to agree on a result before it can be applied.

**Raft alogorithm**
leader election  
log replication  
safety  

**How to choose a leader**
The process of choosing a leader from a pool of machines.  
Leader election is the process of determining a process as the manager of some task distributed among several processes   

**Why leader**
Centralized control simplifies data and task synchronization.  
It is a single point of failure, but solution is to choose a new leader upon failure.  
Many algorithms for leader election.  

**when leader election**
During system startup or when an existing leader fails reported by either its own heartbeat or its clients.  
A client that gets no response from the leader for a predefined time-out interval suspects a failure and initiates leader election.  

**Raft Noval features**
Strong Leader  
Log entries only flow from the leader to other servers.  
Easier management of the replicated log.  

Leader Election  
Raft uses randomized timers to elect leaders.  
Likewise to other algorithms, heartbeat is required.  

Membership Changes  
Raft uses joint consensus approach where the majorities of two different configurations overlap during transitions.  
This allows the cluster to continue operation normally during configuration changes.  

**Three roles**  
The Leader  
The Follower  
The Candidate  


At any given time each server is in one of the above three states.  
In a normal operation, there is exactly one leader!  

The candidate will request for vote from the other nodes  
The other nodes will check their log and if it matches the requesting node's log they cast their vote.   
If the node gets majority votes it becomes the leader  
The leader will replicate the logs   
Checks heartbeats of other nodes  
When the leader dies the other nodes will have arbitrary timeouts. The node which finishes its timeout will nominate itself as a leader and requests for votes  


**Non Consensus approach**
Consistency as Logical Monotonicity  

Monotonicity: 
If a block of code satisfies a simple property: adding things to the input can only increase the output.  

Non Monotonic:  
A block of code may need to “retract” a previous output if more is added to its input.  
logically monotonic distributed code is eventually consistent without any need for coordination protocols (distributed locks, two-phase commit, paxos, raft, etc.) meaning non-consensus.  
eventual consistency can be guaranteed in any program by protecting non-monotonic statements with coordination protocols.  

Consistency without consensus = CRDT  

**Advantages of shared memory**  
Implicit communication  
Low overhead when cached  

**Adv of MQ**
Explicit communication (send/receive)  
Easier to control data placement  

**Disadv of SM**    
Complex to build scalable system  
Requires synchronization  
Hard to control data placement within caching system  

**Disadv of MQ**  
Message passing overhead can be quite high.  
More complex to program  
Introduces question of reception technique (interrupts/polling)  

**SPMD**  
Single Program Multiple Data: the same program runs against multiple data on each processor or node.  
Initialize  
Split data correctly and evenly  
Run the same program  
Combine the results  
Finalize  
Not supported for dynamic load balancing  

**Master worker**  
 Particularly relevant for problems using task  parallelism pattern where task have no dependencies
 Embarrassingly parallel problems
 Main challenge is determining when the entire problem is complete 

Future can be used to load lengthy computation that can be started before the results are needed.

How to choose a design pattern that facilitates the mapping of tasks to units of execution?  

1. Organize by tasks
2. Organize by data decomposition
3. Organize by flow of data


A program can be sped up by adding computing resources, based on proportion of serial and parallelizable components.
p = fraction of work that can be parallelized
n = the number of processor

Speedup =   old running time/new running time

**3 keys to parallel performance**
Coverage of parallelism in algorithm
Amdahl’s Law
Granularity of partitioning among CPUs.
Communication cost and load balancing
Locality of computation and communication
Communication between CPUs or between CPUs and their memories.

**Performance considerations**
For computation-intensive (CPU-bound) tasks that do no I/O and access no shared data, 
Ncpu or Ncpu + 1 threads  optimal throughput 
More threads can degrade performance as the threads compete for CPU and memory resources.

Load balancing factors 
Tasks costs
all tasks have equal (unit) cost or not?
Tasks dependencies
tasks can execute in any order or have a predictable/dynamic structure?
Locality
Zero, regular, irregular communications among tasks





**Anti-entropy**
Each Node “n” periodically contacts a random peer “p” selected from the pool.
Then, n-p engages in an information exchange protocol: n to p (push), n from p (pull), or both push-pull.

**Rumor mongering**
Nodes are initially ignorant.
When an update is received by a node, it becomes a hot rumor.
While a node holds a hot rumor, it periodically chooses a random peer from the pool and sends (push) the rumor to it.
Eventually, a node will lose interest in spreading the rumor.

**Gossip protocol**
Each node in the system periodically exchanges information with a subset of nodes selected randomly.
Complete membership table is unrealistic in a large scale dynamic cluster.
Instead, each node maintains a small local membership table that provides a partial view on the complete set of nodes.
Periodically refreshes the table using a gossiping procedure.


