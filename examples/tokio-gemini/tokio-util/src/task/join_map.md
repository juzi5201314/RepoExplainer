这个文件定义了 `JoinMap` 结构体，它是一个 Tokio 运行时上生成的任务集合，并与哈希映射键相关联。`JoinMap` 类似于 `tokio::task` 中的 [`JoinSet`] 类型，但增加了与每个任务关联的一组键。这些键允许基于它们的键取消 `JoinMap` 中的任务，或者测试 `JoinMap` 中是否存在与给定键对应的任务。此外，当 `JoinMap` 中的任务完成时，它们将返回关联的键以及任务返回的值（如果有）。

**主要组成部分：**

*   **`JoinMap<K, V, S = RandomState>`**:
    *   `K`: 任务的键类型，需要实现 `Hash` 和 `Eq` 特征。
    *   `V`: 任务的返回值类型。
    *   `S`: 哈希构建器类型，默认为 `RandomState`。
    *   `tasks_by_key`:  一个 `HashMap`，用于存储 `AbortHandle`，通过 `Key<K>` 索引。`Key<K>` 包含任务的键和任务 ID，用于解决哈希冲突。
    *   `hashes_by_task`:  一个 `HashMap`，用于存储任务 ID 到其键的哈希值的映射。用于通过任务 ID 进行反向查找。
    *   `tasks`:  一个 `JoinSet`，用于等待在 `JoinMap` 上生成的任务完成。
*   **`Key<K>`**:  一个结构体，包含任务的键 (`K`) 和任务 ID (`Id`)，用于解决哈希冲突。
*   **`JoinMapKeys<'a, K, V>`**:  一个迭代器，用于遍历 `JoinMap` 中的所有键。

**关键方法：**

*   `new()`: 创建一个新的空的 `JoinMap`。
*   `with_capacity(capacity: usize)`: 创建一个具有指定容量的空的 `JoinMap`。
*   `with_hasher(hash_builder: S)`: 创建一个使用给定哈希构建器的空的 `JoinMap`。
*   `with_capacity_and_hasher(capacity: usize, hash_builder: S)`: 创建一个具有指定容量和哈希构建器的空的 `JoinMap`。
*   `len()`: 返回 `JoinMap` 中当前任务的数量。
*   `is_empty()`:  返回 `JoinMap` 是否为空。
*   `capacity()`:  返回 `JoinMap` 的容量。
*   `spawn(key: K, task: F)`:  生成提供的任务，并使用提供的键将其存储在此 `JoinMap` 中。如果先前存在具有此键的任务，则取消并替换它。
*   `spawn_on(key: K, task: F, handle: &Handle)`: 在提供的运行时上生成提供的任务，并使用提供的键将其存储在此 `JoinMap` 中。
*   `spawn_blocking(key: K, f: F)`: 在阻塞线程池上生成阻塞代码，并使用提供的键将其存储在此 `JoinMap` 中。
*   `spawn_blocking_on(key: K, f: F, handle: &Handle)`: 在提供的运行时的阻塞线程池上生成阻塞代码，并使用提供的键将其存储在此 `JoinMap` 中。
*   `spawn_local(key: K, task: F)`: 在当前的 `LocalSet` 上生成提供的任务，并使用提供的键将其存储在此 `JoinMap` 中。
*   `spawn_local_on(key: K, task: F, local_set: &LocalSet)`: 在提供的 `LocalSet` 上生成提供的任务，并使用提供的键将其存储在此 `JoinMap` 中。
*   `join_next()`: 等待 `JoinMap` 中的一个任务完成，并返回其输出以及与该任务对应的键。
*   `shutdown()`:  取消所有任务并等待它们完成关闭。
*   `abort(key: &Q)`:  取消与提供的 `key` 对应的任务。
*   `abort_matching(predicate: impl FnMut(&K) -> bool)`:  取消所有键与 `predicate` 匹配的任务。
*   `keys()`:  返回一个迭代器，用于遍历此 `JoinMap` 中的所有键。
*   `contains_key(key: &Q)`:  如果此 `JoinMap` 包含与提供的键对应的任务，则返回 `true`。
*   `contains_task(task: &Id)`:  如果此 `JoinMap` 包含具有提供的任务 ID 的任务，则返回 `true`。
*   `reserve(additional: usize)`:  为至少 `additional` 个要在此 `JoinMap` 上生成的任务保留容量，而无需重新分配任务键的映射。
*   `shrink_to_fit()`:  尽可能缩小 `JoinMap` 的容量。
*   `shrink_to(min_capacity: usize)`:  将映射的容量缩小到下限。
*   `abort_all()`:  取消此 `JoinMap` 上的所有任务。
*   `detach_all()`:  从此 `JoinMap` 中删除所有任务，而不取消它们。

**工作原理：**

`JoinMap` 通过 `JoinSet` 管理任务的执行。它使用 `HashMap` 来存储任务的键和 `AbortHandle`，以便能够通过键取消任务。当任务完成时，`JoinSet` 会提供任务的 ID，`JoinMap` 使用此 ID 和存储的哈希值来查找并删除任务的键。

**与其他组件的交互：**

*   与 `tokio::task::JoinSet` 交互，用于生成和管理任务。
*   使用 `tokio::runtime::Handle` 和 `tokio::task::LocalSet`，允许在特定的运行时或 `LocalSet` 上生成任务。
*   使用 `hashbrown::HashMap` 存储任务的键和 `AbortHandle`。
*   使用 `tokio::task::AbortHandle` 来取消任务。
