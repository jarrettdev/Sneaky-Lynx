var config;

fetch(chrome.runtime.getURL('config.json'))
  .then((response) => response.json())
  .then((json) => (config = json));

function downloadAsTextFile(text) {
  var blob = new Blob([text], { type: 'text/plain' });
  var url = URL.createObjectURL(blob);
  var a = document.createElement('a');
  a.href = url;
  a.download = config.downloadFileName;
  a.click();
  URL.revokeObjectURL(url);
}

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "getConfig") {
    sendResponse({ config: config });
  }
  if (request.action === "extract") {
    console.log('extracting');
    fetch('http://localhost:5000/api/openai', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt: request.text })
    })
      .then(response => response.json())
      .then(data => {
        let existingResults = localStorage.getItem('responses') || "";
        localStorage.setItem('responses', existingResults + "\n" + data.result);
      })
      .catch(error => console.error('Error:', error));
  }
  if (request.action === "download") {
      let responses = localStorage.getItem('responses');
      downloadAsTextFile(responses);
  }
  if (request.action === "clear") {
      localStorage.removeItem('responses');
      console.log('Data cleared');
  }
});
