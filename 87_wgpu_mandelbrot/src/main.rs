use test1::run;

fn main() {
    // Note: ::block_on can not be used inside async code if wasm should be supported 
    pollster::block_on(run());
}
