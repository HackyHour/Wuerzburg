# HackyHour 87 - GPU rendered Mandelbrot Set

GPU powered [Mandelbrot set](https://en.wikipedia.org/wiki/Mandelbrot_set) rederer, using [wgpu](https://wgpu.rs) - a cross plattform rust library for WebGPU API, also compiling to WASM.

## Setup

- Working rust installation, install trough [rustup](https://rustup.rs)
- [wasm-pack](https://rustwasm.github.io/wasm-pack/) for building web version
 `cargo install wasm-pack`

## Build

### local

```sh
cargo run
```

### wasm

```sh
wasm-pack build --target web 
```

##### running local webserver using python

```sh
python -m http.server 8080
```

-> available on [localhost](http://127.0.0.1:8080/)


## Recources

- [sotrh/learn-wgpu](https://sotrh.github.io/learn-wgpu/)
- [wasm-bindgen guide](https://rustwasm.github.io/docs/wasm-bindgen/introduction.html)
- [WebGPU API reference](https://gpuweb.github.io/gpuweb/)
- [wgpu](https://wgpu.rs/)
- [tour of wgsl](https://google.github.io/tour-of-wgsl/)
