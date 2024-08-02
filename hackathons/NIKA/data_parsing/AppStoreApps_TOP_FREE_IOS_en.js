import store from 'app-store-scraper';
import fs from 'fs';

const categories = [
  store.category.GAMES, store.category.GAMES_ACTION, store.category.GAMES_ADVENTURE,
  store.category.GAMES_ARCADE, store.category.GAMES_BOARD, store.category.GAMES_CARD,
  store.category.GAMES_CASINO, store.category.GAMES_CASUAL, store.category.GAMES_EDUCATIONAL,
  store.category.GAMES_MUSIC, store.category.GAMES_PUZZLE, store.category.GAMES_RACING,
  store.category.GAMES_ROLE_PLAYING, store.category.GAMES_SIMULATION, store.category.GAMES_SPORTS,
  store.category.GAMES_STRATEGY, store.category.GAMES_TRIVIA, store.category.GAMES_WORD,
  store.category.FAMILY, store.category.FAMILY_ACTION, store.category.FAMILY_BRAINGAMES,
  store.category.FAMILY_CREATE, store.category.FAMILY_EDUCATION, store.category.FAMILY_MUSICVIDEO,
  store.category.FAMILY_PRETEND
];

const fetchData = async () => {
  const allApps = [];

  for (const category of categories) {
    for (let page = 0; page < 36; page++) {  // 18 страниц по 200 элементов = 3600 приложений
      try {
        const apps = await store.list({
          category: category,
          collection: store.collection.TOP_FREE_IOS,
          num: 200,  // Максимально разрешенное количество
          page: page + 1,  // Переход на следующую страницу
          fullDetail: true
        });

        for (const app of apps) {
          try {
            console.log(`Fetching details for: ${app.title}`);
            const appDetails = await store.app({ id: app.id });
            allApps.push(appDetails);
          } catch (error) {
            console.error(`Error fetching details for appId: ${app.id}`, error);
          }
        }
      } catch (error) {
        console.error(`Error fetching list for category: ${category}, page: ${page + 1}`, error);
      }
    }
  }

  // Сохранение данных в файл
  fs.writeFileSync('AppStoreApps_TOP_FREE_IOS_en.json', JSON.stringify(allApps, null, 2));
};

fetchData().catch(console.error);
