fn sub2() -> i32 {
    let x = 2;
    return x;
}
fn sub() -> i32 {
    let x = sub2() + sub2();
    let z = x + 10;
    return z;
}
fn params(x: i32) -> i32 {
    let y = x + 1;
    return y;
}

fn main() -> i32 {
    let x = 12;
}
