const rp = require('request-promise');
const $ = require('cheerio');
const URL = 'https://golem.de';

async function get() {

  let html = await rp(URL);
  let items = [];

  let elements = $('.list-articles li', html);

  for (let i = 0; i < 5; i++) {
    let e = elements[i];

    let heading = $(e).find('header > a > div > hgroup >.head2').text();

    let contentEl = $(e).find('p').first();
    contentEl.find('em').remove();
    let content = contentEl.text()
      .replace("Hinweis: Um sich diesen Artikel vorlesen zu lassen, klicken Sie auf den Player im Artikel.", '')
      .trim();

    let href = $(e).find('a')[0].attribs.href;

    items.push({
      heading,
      content,
      href
    });
  }

  let feedItems = items.map(item => {
    return {
      uid: item.heading,
      updateDate: (new Date().toISOString()),
      titleText: item.heading,
      mainText: item.heading + ": " + item.content,
      redirectionUrl: item.href
    };
  });

  return JSON.stringify(feedItems);
}

module.exports = get;
