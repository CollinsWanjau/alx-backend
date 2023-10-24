# 0x01. Caching

## Learning Objectives

*   What a caching system is
*   What FIFO means
*   What LIFO means
*   What LRU means
*   What MRU means
*   What LFU means
*   What the purpose of a caching system
*   What limits a caching system have

## Cache replacement policies

- Cache replacement polices/ Cache replacement algorithms/ Cache algorithms are optimizing instructions or algorithms which a computer program or hardware-maintaned structure can utilize to manage a cache of information. Such algorithms are used in the various components of caching system architecture viz. the processor cache, disk cache, web cache, etc. to manage the contents of the cache, so as to minimize the cache miss rate and overall access time.

### Overview

- `T = m * Tm + Th + E`

- where `m` is the miss rate = 1 - (hit ratio), `Tm` = time to make main-memory access when there is a miss(or, with a multilevel cache, ave. memory ref. time for the next-lower cache), `Th` = latency: time to reference the cache (should be the same for   hits and misses), `E` = secondary effects, such as queing effects in multiprocessor systems.

- `Tm` is the time to make a main-memory access when there is a miss. This is the time to bring the block into the cache, plus the time to do the memory reference that caused the miss. If the cache is multilevel, this is the average memory reference time for the next-lower cache.

- A cache has two primary figures of merit: latency and hit ratio. A number of secondary effects also affect cache design, but these are not as important as the primary effects. The primary effects are:

- The hit ratio of a cache describes how often a searched-for item is found. More efficient policies track more usage info to improve the hit rate for a given cache size.The latency of a cache describes how long after requesting a desired item the cache can return that item when there is a hit.

- Hit-rate measurments are typically performed on bechmark apps, and the hit ratio varies by application.

- Video and audio streaming apps often have a hit ratio of 0%, because each frame of video or audio is used only once. In contrast, a database app may have a hit ratio of 99%.

- The hit ratio is a function of the cache size. As the cache size increases, the hit ratio increases. However, the hit ratio does not increase linearly with cache size. Instead, it increases logarithmically.

- Many cache algorithms (particularly LRU) allow streaming data to fill the cache, pushing out info. which will soon be used again.

- One of the limitations of cache replacement policies, particularly LRU, is that they can suffer from cache pollution. This occurs when streaming data fills up the cache, pushing out information that will soon be used again. As a result, the cache miss rate can increase, reducing the effectiveness of the cache. To mitigate this issue, some cache algorithms use a combination of LRU and other techniques, such as LFU (Least Frequently Used) or MRU (Most Recently Used), to better manage the contents of the cache.

- Algorithms also maintain cache coherence when several caches are used for the same data, such as multiple dbs servers updating a shared data file.

- Maintaining cache coherence is an important consideration when multiple caches are used for the same data, such as in a distributed system with multiple database servers updating a shared data file. In this scenario, it's important to ensure that all caches have a consistent view of the data to prevent inconsistencies or conflicts. This can be achieved through various techniques, such as invalidation-based protocols or update-based protocols, which ensure that all caches are updated with the latest version of the data.

## Policies

### Belady's algorithm

- The most efficient caching algorithm would be to discard information which would not be needed for the longest time; this is known as Belady's optimal algorithm, optimal replacement policy, or Clairvoyant algorithm. Since it is generally impossible to predict how far in the future information will be needed, this algorithm is impractical for real-world use. It is used as a comparison for other algorithms, which are then compared against optimal.

### Simple queue-based policies

#### First in First out(FIFO)

- The simplest method is to discard the information that has been in the cache the longest. This algorithm is called first in first out (FIFO). FIFO is a special case of a more general algorithm called a queue replacement algorithm. In FIFO, the cache behaves as a circular queue. The algorithm discards the oldest information in the cache. This algorithm is easy to implement, but is not optimal in either of the two following ways:

- It does not take into account the frequency with which an item is accessed (see Least frequently used (LFU) below). For example, the algorithm may discard items that are used often if they were requested early in the history.

- It does not take into account the number of times an item is accessed in the recent past (see Least recently used (LRU) below). For example, the algorithm may retain items that are seldom-used overall, but are used often at certain times.

#### Last in First out(LIFO) or First in Last out(FILO)

- The cache evicts the block added most recently first, regardless of how often or how many times it was accessed before. This algorithm is easy to implement and it performs well in real-world applications. For example, web browsers use this policy to keep track of recently visited sites. When the user hits the back button, a recently visited site will be retrieved from the cache and not from the network.

- The last in first out (LIFO) cache replacement algorithm discards the most recently added entry first. This approach is used in stack-based memory allocation. It is easy to implement, but is not optimal.

### Simple recency-based policies

#### Least recently used(LRU)

- Discards the least recently used items first. This algorithm requires keeping track of what was used when, which is expensive if one wants to make sure the algorithm always discards the least recently used item. General implementations of this technique require keeping "age bits" for cache-lines and track the "Least Recently Used" cache-line based on age-bits. In such an implementation, every time a cache-line is used, the age of all other cache-lines changes. LRU is actually a family of caching algorithms with members including 2Q by Theodore Johnson and Dennis Shasha, and LRU/K by Pat O'Neil, Betty O'Neil and Gerhard Weikum. A recent variant of LRU named "Low Inter-reference Recency Set" (LIRS) also deals with caching in a virtual memory environment.

- The access sequence for example is A B C D E F:
![Alt text](Lruexample.png)

- When A B C D is installed in the blocks with sequences numbers (increment 1 for each new access) and E is accessed, it is a miss and must be installed in the block.

- With the LRU algo, E will replace A because A has the lowest rank (A(0)).In the next-to-last step, D is 
accessed and the sequence number is updated. F is then accessed, replacing B - which had the lowest rank.

#### Most-recently-used (MRU)

- Unlike LRU, MRU discards the most-recently-used items first.

- MRU cache algorithms have more hits than LRU due to their tendency to retain older data.[9] MRU algorithms are most useful in situations where the older an item is, the more likely it is to be accessed.

- MRU algos are most useful in situations where the older an item is, the more likely it is to be accessed.
The access sequence for example is A B C D E F:

![Alt text](Mruexample.png)

- A B C D are placed in the cache, since there is space available.
- At the fifth access (E), the block which held D is replaced with E since this block was used most recently.
- At the next access (to D), C is replaced since it was the block accessed just before D.

- MRU is a good replacement policy for a cache that is used to hold instructions or data that are likely to be accessed again in the near future. For example, a web browser that caches web pages that the user has recently accessed may benefit from MRU caching, since the user is likely to want to re-visit those pages sooner than the ones they haven't accessed recently.