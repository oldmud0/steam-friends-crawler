# Algorithm

In order to calculate the number of "steps" between two Steam profiles, we will need to create a network from the friend lists from all public Steam profiles (that's a lot of people!), and then find an optimal path between the two profiles.

This is only intended to work on the public, mainstream Steam community.

## Crawler

The crawler populates the database, which looks like this:
```
[{id: 76561198014872225, friends: [76561198039982559, 76561198035573398, ...], private: false},
...]
```
where `id` represents a profile's 64-bit SteamID, `friends` is a list of 64-bit SteamIDs of that profile's friends, and `private` denotes whether or not the profile was private at crawl time.

The crawler works on a "task" system: it will crawl starting from a specific root node and work its way through the entire network until there are no more profiles left uncrawled, in which case the task is completed and the next one can be begun.

The root node must not be a ghost or an orphan.

### Ghosts
Ghosts are profiles that cannot be crawled because they are private. Instead, we can only infer their friends list from public profiles that have a ghost added as their friends list. A ghost can be "revealed" by developing a profile of the ghost only after the crawling process has concluded, in which SteamIDs that are mentioned in friends lists but that do not have their own entry in the database are created one with `private: true`, and the ghost's inferred friends list must be constructed by looking up all profiles which have the ghost on their friends list.

### Orphans
Orphans are profiles that are public, but cannot be reached even indirectly because they do not have any public friends.

### True orphans
True orphans have the properties of both ghosts and orphans: they are private and friendless. These are to be pruned from the database.

### Clusters
In a perfect world, all ~170 million public Steam profiles would be interconnected in a massive network. However, this is not what may occur in practice. Therefore, our network will have to be divided into clusters.

#### Main/mainstream
The main cluster is the interconnected majority of all Steam profiles. Most of the time, it does not matter which root node is chosen to crawl the main cluster.

#### Offbeat/out-of-band
Offbeat clusters are not connected to the main cluster, making them difficult to detect due to their remoteness. It is likely that they are connected to the main cluster by a ghost, but in this case, an offbeat cluster would not be detected at all, since it would be impossible to find any profiles on such a cluster and, if a crawling job was performed where the root node was inside this offbeat cluster, the cluster would immediately merge with the main cluster.

True offbeat clusters have no connection to the main cluster and can be tracked as "niche" groups. The only way to find such groups would be to find queries (after the database has matured) coming from the frontend where a SteamID exists in the community but not in the database. You could also throw darts and "guess" SteamIDs, but this would obviously be too impractical.

### Overview of the algorithm
 - Start from a designated root node/profile.
 - Get profile's friends.
 - Record profile + friends on database (`private: false`).
 - For each friend:
    - Crawl friend.
        - If friend is private, record profile, `private: true`, and add parent as friend.
        - If friend is already in database, skip.
        - Else, crawl recursively as above.
 - Go up until the root node is about to be returned.

### Post-crawl
 - Parse list of unknown profiles sent up by the frontend.
    - If the unknown profile is not in database, make a special crawl job for it:
        - Tag new profiles added during the crawl.
        - If it never connected with any profiles that were not tagged, move the tagged profiles including root node to a new cluster.
        - Untag the new profiles since the tag was merely temporary.

Every 12 hours, create a snapshot of the database.

### Updating
 - Crawl every existing profile on the database, smallest clusters first.
 - If any profile in a cluster connects with another profile in another cluster, merge them together.

## Pathfinding

### Overview of the algorithm
Every 6 hours, grab the latest snapshot of the database.

 - If A and/or B are not in the database:
    - Send the crawler the SteamID of A and/or B for further processing.
    - Fail, stating that one of the profiles could not be found.
 - If A and B are on different clusters:
    - Fail, stating that a path between A and B is impossible.
 - NetworkX does most of the job.

### Avoid treading on ghosts
When an option such as `Avoid treading on ghosts` is checked, then a weighted pathfinder is activated which sets the weight of ghost nodes to -5,000. In essence, if a path exists that involves up to 5,000 non-ghost nodes, then it is favored over one that includes one ghost node, even if the one with the ghost node is more optimal. However, if the path that includes the ghost node is the only possible path to a profile, then that path is chosen.