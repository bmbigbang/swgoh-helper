const ApiSwgohHelp = require('api-swgoh-help');
const statCalculator = require('swgoh-stat-calc');

// @ts-ignore
import gameData from "./gameData.json";
import environment from "../env.json";
import fs from "fs";

statCalculator.setGameData( gameData );

const swapi = new ApiSwgohHelp({
	"username": environment.username,
	"password": environment.password
});

async function unit_stat_lookup() {
  // get Player roster from api.swgoh.help
  let player
  try {
    const response = await swapi.fetchPlayer({
      allycode: environment.allycode,
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

  for (let i = 0; i < player.roster.length; i++) {
    let unit = player.roster[i]

    if (unit.combatType != 1) {
      continue
    }
    try {
      unit_stats[unit.defId] = statCalculator.calcCharStats( unit, {
        withoutModCalc: true,
        percentVals: false,
        gameStyle: false
      } );
    } catch(error) {
      console.log(unit)
      console.error(error)
    }

    try {
      unit_stats[unit.defId] = {
        ...unit_stats[unit.defId],
        ...statCalculator.calcCharStats( unit, {
          withoutModCalc: true,
          percentVals: true,
          gameStyle: true
        } )
      };
    } catch(error) {
      console.log(unit)
      console.error(error)
    }
  }
  try {
    await fs.promises.writeFile(
      'unit_stat_data.json',
      JSON.stringify(unit_stats, null, "    ")
    );
  } catch (error) {
    throw error
  }

  process.exit(0);
}

unit_stat_lookup()

export { unit_stat_lookup }