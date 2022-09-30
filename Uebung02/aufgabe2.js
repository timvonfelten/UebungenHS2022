function wuerfel() {
    const wuerfel = [1, 2, 3, 4, 5, 6];
    const random = Math.floor(Math.random() * wuerfel.length);
    return random+1;
    }
    r = wuerfel()
    console.log(r)