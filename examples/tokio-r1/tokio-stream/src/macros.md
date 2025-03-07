### Code File Explanation: `tokio-stream/src/macros.rs`

#### Purpose
This file defines Rust macros for **conditional compilation** based on Tokio's feature flags. These macros enable or disable specific code blocks and documentation depending on which features (e.g., `fs`, `net`, `sync`) are enabled during compilation. They ensure feature-gated code is included only when needed and properly documented.

#### Key Components
1. **Feature-Specific Macros**:
   - Macros like `cfg_fs`, `cfg_net`, `cfg_sync`, etc., wrap code blocks with `#[cfg(feature = "...")]` attributes. For example:
     ```rust
     macro_rules! cfg_fs {
         ($($item:item)*) => {
             $(
                 #[cfg(feature = "fs")] // Includes code only if "fs" feature is enabled
                 #[cfg_attr(docsrs, doc(cfg(feature = "fs")))] // Documents feature requirement
                 $item
             )*
         }
     }
     ```
   - Each macro corresponds to a Tokio feature (e.g., `fs` for filesystem utilities, `net` for networking).

2. **Documentation Handling**:
   - The `#[cfg_attr(docsrs, ...)]` attribute ensures feature-gated items appear in documentation **only** when the feature is active (used by `docs.rs`).

3. **Code Organization**:
   - Macros streamline conditional compilation without cluttering code with repetitive `#[cfg]` attributes. For example, code for `io-util` is grouped under `cfg_io_util!`.

#### Relationship to Project
- **Modularity**: Tokio uses feature flags to allow users to include only necessary components (reducing build time and dependencies). This file centralizes the logic for feature-gated code in `tokio-stream`.
- **Documentation Accuracy**: Ensures documentation reflects active features, avoiding confusion for users.
- **Consistency**: Reused across the Tokio ecosystem (e.g., `cfg_net` in `tokio-stream` aligns with similar macros in other Tokio crates).

#### Example Usage
When the `net` feature is enabled, code inside `cfg_net! { ... }` becomes active:
```rust
cfg_net! {
    pub struct TcpStream { ... } // Only compiled if `net` is enabled
}
```

---
