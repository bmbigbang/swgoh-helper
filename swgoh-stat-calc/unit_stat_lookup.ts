const ApiSwgohHelp = require('api-swgoh-help');
const statCalculator = require('swgoh-stat-calc');

import gameData from "./gameData.json";
import ENV from "../env.json";
import fs from "fs";

statCalculator.setGameData( gameData );

const swapi = new ApiSwgohHelp({
	"username": ENV.username,
	"password": ENV.password
});

async function unit_stat_lookup() {
  // get Player roster from api.swgoh.help
  let player
  try {
    const response = await swapi.fetchPlayer({
      allycode: ENV.allycode,
      language: "ENG_US",
      project: {
        roster: {
          defId: 1,
          nameKey: 1,
          rarity: 1,
          level: 1,
          gear: 1,
          equipped: 1,
          combatType: 1,
          skills: 1,
          mods: 1,
          relic: 1
        }
      }
    });
    player = response.result[0]
  } catch (error) {
    console.error(error)
  }

  let unit_stats: Record<string, any> = {};
  player.roster.forEach( (unit: any) => {
    if (unit.combatType != 1) {
      return
    }
    try {
      unit_stats[unit.defId] = statCalculator.calcCharStats( unit, {
        withoutModCalc: true,
        percentVals: true,
        gameStyle: true
      } );
    } catch(error) {
      console.log(unit)
      console.error(error)
    }

  });

  fs.writeFile("unit_stat_data.json", JSON.stringify(unit_stats, null, "    "), "utf-8", (err) => console.error(err))
}

unit_stat_lookup()

export { unit_stat_lookup }