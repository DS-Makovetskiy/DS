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
  let appCount = 0;
  let fileIndex = 1;
  const detailedApps = [];

  const saveDataToFile = async (apps, index) => {
    const filePath = `../data/AppStoreApps_NEW_FREE_IOS_ru_${String(index).padStart(3, '0')}.json`;
    fs.writeFileSync(filePath, JSON.stringify(apps, null, 2));
  };

  for (const category of categories) {
    for (let page = 0; page < 50; page++) {  // 50 страниц по 200 элементов = 10000 приложений
      try {
        const apps = await store.list({
          category: category,
          collection: store.collection.NEW_FREE_IOS,
          num: 200,  // Максимально разрешенное количество
          page: page + 1,  // Переход на следующую страницу
          lang: 'RU',
          country: 'RU',
          fullDetail: true
        });

        for (const app of apps) {
          try {
            console.log(`Fetching details for: ${app.title}`);
            const appDetails = await store.app({ id: app.id });
            detailedApps.push(appDetails);
            appCount++;

            if (appCount % 200 === 0) {
              await saveDataToFile(detailedApps.splice(0, 200), fileIndex);
              fileIndex++;
            }
          } catch (error) {
            console.error(`Error fetching details for appId: ${app.id}`, error);
          }
        }
      } catch (error) {
        console.error(`Error fetching list for category: ${category}, page: ${page + 1}`, error);
      }
    }
  }

  // Save any remaining apps
  if (detailedApps.length > 0) {
    await saveDataToFile(detailedApps, fileIndex);
  }
};

fetchData().catch(console.error);




// V2
// import store from 'app-store-scraper';
// import fs from 'fs';

// const categories = [
//   store.category.GAMES, store.category.GAMES_ACTION, store.category.GAMES_ADVENTURE,
//   store.category.GAMES_ARCADE, store.category.GAMES_BOARD, store.category.GAMES_CARD,
//   store.category.GAMES_CASINO, store.category.GAMES_CASUAL, store.category.GAMES_EDUCATIONAL,
//   store.category.GAMES_MUSIC, store.category.GAMES_PUZZLE, store.category.GAMES_RACING,
//   store.category.GAMES_ROLE_PLAYING, store.category.GAMES_SIMULATION, store.category.GAMES_SPORTS,
//   store.category.GAMES_STRATEGY, store.category.GAMES_TRIVIA, store.category.GAMES_WORD,
//   store.category.FAMILY, store.category.FAMILY_ACTION, store.category.FAMILY_BRAINGAMES,
//   store.category.FAMILY_CREATE, store.category.FAMILY_EDUCATION, store.category.FAMILY_MUSICVIDEO,
//   store.category.FAMILY_PRETEND
// ];

// const fetchData = async () => {
//   const filePath = '../data/AppStoreApps_NEW_FREE_IOS_ru.json';
//   const tempFilePath = `${filePath}.temp`;

//   // Проверка, существует ли основной файл, и если нет, создание его с пустым массивом
//   if (!fs.existsSync(filePath)) {
//     fs.writeFileSync(filePath, '[]');
//   }

//   for (const category of categories) {
//     for (let page = 0; page < 50; page++) {  // 50 страниц по 200 элементов
//       try {
//         const apps = await store.list({
//           category: category,
//           collection: store.collection.NEW_FREE_IOS,
//           num: 200,  // Максимально разрешенное количество
//           page: page + 1,  // Переход на следующую страницу
//           lang:       'ru',
//           country:    'ru',
//           fullDetail: true
//         });

//         for (const app of apps) {
//           try {
//             console.log(`Fetching details for: ${app.title}`);
//             const appDetails = await store.app({ id: app.id });
            
//             // Чтение текущего содержимого основного файла
//             const currentData = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
            
//             // Добавление нового приложения к данным
//             currentData.push(appDetails);
            
//             // Запись данных во временный файл
//             fs.writeFileSync(tempFilePath, JSON.stringify(currentData, null, 2));
            
//             // Перемещение временного файла на место основного файла
//             fs.renameSync(tempFilePath, filePath);
//           } catch (error) {
//             console.error(`Error fetching details for appId: ${app.id}`, error);
//           }
//         }
//       } catch (error) {
//         console.error(`Error fetching list for category: ${category}, page: ${page + 1}`, error);
//       }
//     }
//   }
// };

// fetchData().catch(console.error);


// V1
// import store from 'app-store-scraper';
// import fs from 'fs';

// const categories = [
//   store.category.GAMES, store.category.GAMES_ACTION, store.category.GAMES_ADVENTURE,
//   store.category.GAMES_ARCADE, store.category.GAMES_BOARD, store.category.GAMES_CARD,
//   store.category.GAMES_CASINO, store.category.GAMES_CASUAL, store.category.GAMES_EDUCATIONAL,
//   store.category.GAMES_MUSIC, store.category.GAMES_PUZZLE, store.category.GAMES_RACING,
//   store.category.GAMES_ROLE_PLAYING, store.category.GAMES_SIMULATION, store.category.GAMES_SPORTS,
//   store.category.GAMES_STRATEGY, store.category.GAMES_TRIVIA, store.category.GAMES_WORD,
//   store.category.FAMILY, store.category.FAMILY_ACTION, store.category.FAMILY_BRAINGAMES,
//   store.category.FAMILY_CREATE, store.category.FAMILY_EDUCATION, store.category.FAMILY_MUSICVIDEO,
//   store.category.FAMILY_PRETEND
// ];

// const fetchData = async () => {
//   const allApps = [];

//   for (const category of categories) {
//     for (let page = 0; page < 36; page++) {  // 18 страниц по 200 элементов = 3600 приложений
//       try {
//         const apps = await store.list({
//           category: category,
//           collection: store.collection.NEW_FREE_IOS,
//           num: 200,  // Максимально разрешенное количество
//           page: page + 1,  // Переход на следующую страницу
//           lang:       'ru',
//           country:    'ru',
//           fullDetail: true
//         });

//         for (const app of apps) {
//           try {
//             console.log(`Fetching details for: ${app.title}`);
//             const appDetails = await store.app({ id: app.id });
//             allApps.push(appDetails);
//           } catch (error) {
//             console.error(`Error fetching details for appId: ${app.id}`, error);
//           }
//         }
//       } catch (error) {
//         console.error(`Error fetching list for category: ${category}, page: ${page + 1}`, error);
//       }
//     }
//   }

//   // Сохранение данных в файл
//   fs.writeFileSync('AppStoreApps_NEW_FREE_IOS_ru.json', JSON.stringify(allApps, null, 2));
// };

// fetchData().catch(console.error);
