import gplay from 'google-play-scraper';
import { createObjectCsvWriter as createCsvWriter } from 'csv-writer';
import fs from 'fs';

async function getAppData(appId) {
    try {
        console.log(`Получение данных для ${appId}`);
        const appData = await gplay.app({ appId });
        return appData;
    } catch (error) {
        console.error(`Ошибка получения данных для ${appId}:`, error);
    }
}

async function getTopApps() {
    console.log('Получение списка топовых приложений');
    const allApps = [];

    const years = ['2024', '2023'];
    for (const year of years) {
        console.log(`Получение данных за ${year} год`);
        const topApps = await gplay.list({
            collection: gplay.collection.TOP_FREE,
            num: 50,
            fullDetail: true,
            year: year
        });
        allApps.push(...topApps);
    }

    return allApps;
}

async function writeDataToCSV(data) {
    console.log('Запись данных в CSV');
    const csvWriter = createCsvWriter({
        path: 'google_play_apps.csv',
        header: [
            { id: 'title', title: 'Title' },
            { id: 'appId', title: 'App ID' },
            { id: 'url', title: 'URL' },
            { id: 'score', title: 'Score' },
            { id: 'reviews', title: 'Reviews' },
            { id: 'installs', title: 'Installs' },
            { id: 'free', title: 'Free' },
            { id: 'developer', title: 'Developer' },
            { id: 'updated', title: 'Updated' }
        ]
    });

    await csvWriter.writeRecords(data);
    console.log('Данные успешно сохранены в google_play_apps.csv');
}

(async () => {
    console.log('Начало выполнения скрипта');
    const topApps = await getTopApps();
    await writeDataToCSV(topApps);
    console.log('Скрипт завершен');
})();
