import store from 'app-store-scraper';
import fs from 'fs';
import path from 'path';
import archiver from 'archiver';
import { Worker, isMainThread, parentPort, workerData } from 'worker_threads';
// import { Queue } from 'async';
import async from 'async';
const { queue } = async;

const collections = [
  "NEW_FREE_IOS", "NEW_IOS", "NEW_PAID_IOS", "TOP_FREE_IOS", "TOP_FREE_IPAD",
  "TOP_GROSSING_IOS", "TOP_GROSSING_IPAD", "TOP_PAID_IOS", "TOP_PAID_IPAD"
];

const saveDataToFile = async (apps, collection, index) => {
  const dirPath = path.join('data');
  if (!fs.existsSync(dirPath)) {
    fs.mkdirSync(dirPath, { recursive: true });
  }
  
  const fileName = `AppStoreApps_${collection}_ru_${String(index).padStart(3, '0')}.json`;
  const filePath = path.join(dirPath, fileName);
  fs.writeFileSync(filePath, JSON.stringify(apps, null, 2));
  
  const zipFilePath = `${filePath}.zip`;
  const output = fs.createWriteStream(zipFilePath);
  const archive = archiver('zip', { zlib: { level: 9 } });
  
  output.on('close', () => {
    fs.unlinkSync(filePath);  // Удаление оригинального файла
  });
  
  archive.pipe(output);
  archive.file(filePath, { name: fileName });
  await archive.finalize();
};

const workerQueue = queue(async (task, done) => {
  try {
    await saveDataToFile(task.apps, task.collection, task.index);
    done();
  } catch (error) {
    console.error(`Error saving data to file: ${error}`);
    done(error);
  }
}, 2); // Максимум 2 файла на сохранение параллельно


const fetchData = async () => {
  for (const collection of collections) {
    let appCount = 0;
    let fileIndex = 1;
    let detailedApps = [];

    for (let page = 0; page < 500; page++) {
      try {
        const apps = await store.list({
          collection: store.collection[collection],
          num: 200,
          page: page + 1,
          lang: 'RU',
          country: 'RU',
          fullDetail: true
        });

        const appPromises = apps.map(async (app) => {
          const appDetails = await store.app({ id: app.id });
          return appDetails;
        });

        const results = await Promise.all(appPromises);
        detailedApps = detailedApps.concat(results);
        appCount += results.length;

        if (appCount >= 4000) {
          workerQueue.push({ apps: detailedApps.splice(0, 4000), collection, index: fileIndex });
          fileIndex++;
          appCount = 0;  // Сброс счётчика для следующей порции данных
        }
      } catch (error) {
        console.error(`Error fetching list for collection: ${collection}, page: ${page + 1}`, error);
      }
    }

    if (detailedApps.length > 0) {
      workerQueue.push({ apps: detailedApps, collection, index: fileIndex });
    }

    // Ожидание завершения всех задач в очереди
    await workerQueue.drain();

    await combineFilesAndArchive(collection);
  }
};

const combineFilesAndArchive = async (collection) => {
  const combinedFilePath = path.join('data', `AppStoreApps_${collection}_ru.json`);
  const output = fs.createWriteStream(combinedFilePath);
  
  output.on('close', () => {
    archiveFile(combinedFilePath);
  });

  fs.readdirSync('data')
    .filter(file => file.includes(`AppStoreApps_${collection}_ru_`) && file.endsWith('.json'))
    .forEach(file => {
      const data = fs.readFileSync(path.join('data', file));
      output.write(data);
      fs.unlinkSync(path.join('data', file));  // Удаление исходного файла
    });

  output.end();
};

const archiveFile = async (filePath) => {
  const output = fs.createWriteStream(`${filePath}.zip`);
  const archive = archiver('zip', { zlib: { level: 9 } });
  
  output.on('close', () => {
    fs.unlinkSync(filePath);  // Удаление оригинального файла
  });
  
  archive.pipe(output);
  archive.file(filePath, { name: path.basename(filePath) });
  await archive.finalize();
};

fetchData().catch(console.error);


















// import store from 'app-store-scraper';
// import fs from 'fs';
// import path from 'path';
// import archiver from 'archiver';

// const collections = [
//   "NEW_FREE_IOS", "NEW_IOS", "NEW_PAID_IOS", "TOP_FREE_IOS", "TOP_FREE_IPAD",
//   "TOP_GROSSING_IOS", "TOP_GROSSING_IPAD", "TOP_PAID_IOS", "TOP_PAID_IPAD"
// ];

// const saveDataToFile = async (apps, collection, index) => {
//   // Создание директории, если она не существует
//   const dirPath = path.join('data');
//   if (!fs.existsSync(dirPath)) {
//     fs.mkdirSync(dirPath, { recursive: true });
//   }
  
//   const fileName = `AppStoreApps_${collection}_ru_${String(index).padStart(3, '0')}.json`;
//   const filePath = path.join(dirPath, fileName);
//   fs.writeFileSync(filePath, JSON.stringify(apps, null, 2));
  
//   // Архивация файла
//   const zipFilePath = `${filePath}.zip`;
//   const output = fs.createWriteStream(zipFilePath);
//   const archive = archiver('zip', { zlib: { level: 9 } });
  
//   output.on('close', () => {
//     fs.unlinkSync(filePath);  // Удаление оригинального файла
//   });
  
//   archive.pipe(output);
//   archive.file(filePath, { name: fileName });
//   await archive.finalize();
// };

// const fetchData = async () => {
//   for (const collection of collections) {
//     let appCount = 0;
//     let fileIndex = 1;
//     const detailedApps = [];

//     for (let page = 0; page < 50; page++) {
//       try {
//         const apps = await store.list({
//           collection: store.collection[collection],
//           num: 200,
//           page: page + 1,
//           lang: 'RU',
//           country: 'RU',
//           fullDetail: true
//         });

//         for (const app of apps) {
//           const appDetails = await store.app({ id: app.id });
//           detailedApps.push(appDetails);
//           appCount++;

//           if (appCount % 2000 === 0) {
//             await saveDataToFile(detailedApps.splice(0, 2000), collection, fileIndex);
//             fileIndex++;
//           }
//         }
//       } catch (error) {
//         console.error(`Error fetching list for collection: ${collection}, page: ${page + 1}`, error);
//       }
//     }

//     if (detailedApps.length > 0) {
//       await saveDataToFile(detailedApps, collection, fileIndex);
//     }

//     // Объединение файлов и их архивирование
//     await combineFilesAndArchive(collection);
//   }
// };

// const combineFilesAndArchive = async (collection) => {
//   const combinedFilePath = path.join('data', `AppStoreApps_${collection}_ru.json`);
//   const output = fs.createWriteStream(combinedFilePath);
  
//   output.on('close', () => {
//     archiveFile(combinedFilePath);
//   });
  
//   fs.readdirSync('data')
//     .filter(file => file.includes(`AppStoreApps_${collection}_ru_`) && file.endsWith('.json'))
//     .forEach(file => {
//       const data = fs.readFileSync(path.join('data', file));
//       output.write(data);
//       fs.unlinkSync(path.join('data', file));  // Удаление исходного файла
//     });

//   output.end();
// };

// const archiveFile = async (filePath) => {
//   const output = fs.createWriteStream(`${filePath}.zip`);
//   const archive = archiver('zip', { zlib: { level: 9 } });
  
//   output.on('close', () => {
//     fs.unlinkSync(filePath);  // Удаление оригинального файла
//   });
  
//   archive.pipe(output);
//   archive.file(filePath, { name: path.basename(filePath) });
//   await archive.finalize();
// };

// fetchData().catch(console.error);















// import store from 'app-store-scraper';
// import fs from 'fs';
// import path from 'path';
// import archiver from 'archiver';

// const collections = [
//   "NEW_FREE_IOS", "NEW_IOS", "NEW_PAID_IOS", "TOP_FREE_IOS", "TOP_FREE_IPAD",
//   "TOP_GROSSING_IOS", "TOP_GROSSING_IPAD", "TOP_PAID_IOS", "TOP_PAID_IPAD"
// ];

// const saveDataToFile = async (apps, collection, index) => {
//   const fileName = `AppStoreApps_${collection}_ru_${String(index).padStart(3, '0')}.json`;
//   const filePath = path.join('data', fileName);
//   fs.writeFileSync(filePath, JSON.stringify(apps, null, 2));
  
//   // Архивация файла
//   const zipFilePath = `${filePath}.zip`;
//   const output = fs.createWriteStream(zipFilePath);
//   const archive = archiver('zip', { zlib: { level: 9 } });
  
//   output.on('close', () => {
//     fs.unlinkSync(filePath);  // Удаление оригинального файла
//   });
  
//   archive.pipe(output);
//   archive.file(filePath, { name: fileName });
//   await archive.finalize();
// };

// const fetchData = async () => {
//   for (const collection of collections) {
//     let appCount = 0;
//     let fileIndex = 1;
//     const detailedApps = [];

//     for (let page = 0; page < 50; page++) {
//       try {
//         const apps = await store.list({
//           collection: store.collection[collection],
//           num: 200,
//           page: page + 1,
//           lang: 'RU',
//           country: 'RU',
//           fullDetail: true
//         });

//         for (const app of apps) {
//           const appDetails = await store.app({ id: app.id });
//           detailedApps.push(appDetails);
//           appCount++;

//           if (appCount % 2000 === 0) {
//             await saveDataToFile(detailedApps.splice(0, 2000), collection, fileIndex);
//             fileIndex++;
//           }
//         }
//       } catch (error) {
//         console.error(`Error fetching list for collection: ${collection}, page: ${page + 1}`, error);
//       }
//     }

//     if (detailedApps.length > 0) {
//       await saveDataToFile(detailedApps, collection, fileIndex);
//     }

//     // Объединение файлов и их архивирование
//     await combineFilesAndArchive(collection);
//   }
// };

// const combineFilesAndArchive = async (collection) => {
//   const combinedFilePath = path.join('data', `AppStoreApps_${collection}_ru.json`);
//   const output = fs.createWriteStream(combinedFilePath);
  
//   output.on('close', () => {
//     archiveFile(combinedFilePath);
//   });
  
//   fs.readdirSync('data')
//     .filter(file => file.includes(`AppStoreApps_${collection}_ru_`) && file.endsWith('.json'))
//     .forEach(file => {
//       const data = fs.readFileSync(path.join('data', file));
//       output.write(data);
//       fs.unlinkSync(path.join('data', file));  // Удаление исходного файла
//     });

//   output.end();
// };

// const archiveFile = async (filePath) => {
//   const output = fs.createWriteStream(`${filePath}.zip`);
//   const archive = archiver('zip', { zlib: { level: 9 } });
  
//   output.on('close', () => {
//     fs.unlinkSync(filePath);  // Удаление оригинального файла
//   });
  
//   archive.pipe(output);
//   archive.file(filePath, { name: path.basename(filePath) });
//   await archive.finalize();
// };

// fetchData().catch(console.error);
