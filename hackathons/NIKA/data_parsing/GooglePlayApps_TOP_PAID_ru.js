import gplay from 'google-play-scraper';
import fs from 'fs';

const categories = [
  'GAME', 'GAME_ACTION', 'GAME_ADVENTURE', 'GAME_ARCADE', 'GAME_BOARD', 'GAME_CARD',
  'GAME_CASINO', 'GAME_CASUAL', 'GAME_EDUCATIONAL', 'GAME_MUSIC', 'GAME_PUZZLE',
  'GAME_RACING', 'GAME_ROLE_PLAYING', 'GAME_SIMULATION', 'GAME_SPORTS',
  'GAME_STRATEGY', 'GAME_TRIVIA', 'GAME_WORD', 'FAMILY', 'FAMILY_ACTION',
  'FAMILY_BRAINGAMES', 'FAMILY_CREATE', 'FAMILY_EDUCATION', 'FAMILY_MUSICVIDEO',
  'FAMILY_PRETEND'
];

const fetchData = async () => {
  const allApps = [];

  for (const category of categories) {
    for (let page = 0; page < 18; page++) {  // 18 страниц по 200 элементов = 3600 приложений
      try {
        const apps = await gplay.list({
          category:   category,
          collection: gplay.collection.TOP_PAID,
          num:        200,  // Максимально разрешенное количество
          page:       page + 1,  // Переход на следующую страницу
          lang:       'ru',
          country:    'ru',
          fullDetail: true
        });

        for (const app of apps) {
          try {
            console.log(`Fetching details for: ${app.title}`);
            const appDetails = await gplay.app({ appId: app.appId });
            allApps.push(appDetails);
          } catch (error) {
            console.error(`Error fetching details for appId: ${app.appId}`, error);
          }
        }
      } catch (error) {
      console.error(`Error fetching list for category: ${category}`, error);
      }
    }
  }

  // Сохранение данных в файл
  fs.writeFileSync('GooglePlayApps_TOP_PAID_ru.json', JSON.stringify(allApps, null, 2));
};

fetchData().catch(console.error);