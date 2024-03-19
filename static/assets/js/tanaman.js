// Function to create HTML for each article
function createArticleHTML(article) {
    return `
      <article class="jkit-post post-${article.id}">
        <div class="jkit-thumb">
          <a href="${article.link}">
            <div class="thumbnail-container">
              <img src="${article.image}" alt="${article.title}" loading="lazy" />
            </div>
          </a>
        </div>
        <div class="jkit-postblock-content">
          <h3 class="jkit-post-title">
            <a href="${article.link}">${article.title}</a>
          </h3>
          <div class="jkit-post-meta">
            <div class="jkit-meta-date icon-position-before">
              <i aria-hidden="true" class="fas fa-clock"></i>${article.date}
            </div>
          </div>
          <div class="jkit-post-meta-bottom"></div>
        </div>
      </article>
    `;
  }
  
// Fetch data from external source
fetch('../../json/penyakit.json')
  .then(response => {
    if (!response.ok) {
      throw new Error(`Failed to fetch data. Status: ${response.status}`);
    }
    return response.json();
  })
  .then(data => {
    // Insert articles into the container
    var articleContainer = document.getElementById("article-container");
    data.forEach(function (article) {
      articleContainer.innerHTML += createArticleHTML(article);
    });
  })
  .catch(error => console.error('Error fetching data:', error));

  