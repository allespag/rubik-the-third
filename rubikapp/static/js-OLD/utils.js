function getRandomArbitrary(min, max) {
    return Math.random() * (max - min) + min;
}

function getRandomKey(collection) {
    let keys = Array.from(collection.keys());
    let index = Math.floor(Math.random() * keys.length);
    return keys[index];
}
