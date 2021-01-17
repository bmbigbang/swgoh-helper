import environment from "../env.json";

const dataBuilder = require('swgoh-stat-calc-data-builder').fromPrefs({
  username: environment.username,
  password: environment.password
});
let path = "./";
dataBuilder.loadData(path).then( (success: boolean) => {
  if (success) {
    console.log(`Saved data to ${path}gameData.json\nVersion: ${JSON.stringify(dataBuilder.getVersion())}`);
    process.exit(0);
  } else {
    console.log('Continuing with outdated data');
    process.exit(1);
  }
});