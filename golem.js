const Axios = require('axios');
const $ = require('cheerio').default;
const URL = 'https://golem.de';

async function request(url) {
  return (await Axios(url, {
    headers: {
      'Cookie': 'golem_consent20=cmp|210630',
    },
    timeout: 10000,
  })).data;
}

async function get() {
  let html = await request(URL);
  let elements = $('.list-articles li', html);
  let elementsToScrape = elements.slice(0, 5).get();
  let items = await Promise.all(elementsToScrape.map(getSingle));

  let feedItems = items
    .map(item => {
      return {
        uid: item.heading,
        updateDate: item.datetime,
        titleText: item.heading,
        mainText: item.heading + ": " + item.content,
        redirectionUrl: item.href,
      };
    })
    .filter(feedItem => !["Sonst noch was?"].includes(feedItem.titleText));

    if (!feedItems.length) {
    	throw new Error('No articles found');
    }

  return feedItems;
}

async function getSingle(e) {
  let heading = $(e).find('header > a > div > hgroup >.head2').text();

  let contentEl = $(e).find('p').first();
  contentEl.find('em').remove();
  let content = contentEl.text()
    .replace("Hinweis: Um sich diesen Artikel vorlesen zu lassen, klicken Sie auf den Player im Artikel.", '')
    .replace(/\s\s+/g, ' ')
    .trim();

  let href = $(e).find('a')[0].attribs.href;

  // visit article to check date
  let articleHtml = await request(href);
  // full path: '#screen > div:nth-child(2) > article > header > div.authors.authors--withsource > time'
  let datetime = $('time', articleHtml).attr('datetime');

  return {
    heading,
    content,
    href,
    datetime,
  };
}

module.exports = get;
