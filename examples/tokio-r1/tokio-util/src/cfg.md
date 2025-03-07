## Code File Explanation: `tokio-util/src/cfg.rs`

### Purpose
This file defines Rust macros for **conditional compilation** based on feature flags in the `tokio-util` crate. It enables modular inclusion of code and documentation depending on which features (e.g., `codec`, `net`, `io`) are enabled during compilation. This optimizes build times and ensures users only compile the code they need.

### Key Components
1. **Feature-Specific Macros**:
   - Macros like `cfg_codec!`, `cfg_net!`, `cfg_io!`, etc., wrap code blocks with `#[cfg(feature = "...")]` attributes. For example:
     ```rust
     macro_rules! cfg_codec {
         ($($item:item)*) => {
             $(
                 #[cfg(feature = "codec")]
                 #[cfg_attr(docsrs, doc(cfg(feature = "codec")))]
                 $item
             )*
         }
     }
     ```
   - The `cfg_attr(docsrs, ...)` attribute ensures documentation on [docs.rs](https://docs.rs) reflects feature-gated items.

2. **Dependent Features**:
   - Some macros require multiple features. For example, `cfg_net!` activates only if both `net` and `codec` are enabled:
     ```rust
     #[cfg(all(feature = "net", feature = "codec"))]
     ```

3. **Nested Macros**:
   - `cfg_io_util!` is nested inside `cfg_io!`, meaning `io-util` depends on the `io` feature:
     ```rust
     cfg_io! {
         macro_rules! cfg_io_util { ... }
     }
     ```

4. **Documentation Handling**:
   - The `cfg_attr(docsrs, ...)` ensures feature-specific documentation is visible on docs.rs, aiding users in understanding feature requirements.

### Integration with the Project
- **Feature Management**: This file centralizes conditional compilation logic, allowing other modules to use these macros instead of scattering `#[cfg]` attributes. For example, network utilities in `tokio-util` might use `cfg_net!` to gate code.
- **Dependency Control**: Macros like `cfg_net!` enforce feature dependencies (e.g., `net` requires `codec`), preventing incomplete or broken builds.
- **Documentation Clarity**: By annotating items with `doc(cfg(...))`, users see exactly which features are needed for specific APIs.

### Role in the Project