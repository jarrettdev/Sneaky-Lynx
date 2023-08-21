chrome.runtime.sendMessage({ action: "getConfig" }, function (response) {
    var config = response.config;
    console.log('config', config)
    if (config.multiclick) {
        console.log('multiclick', config.multiclick);
        var multiclickElements = document.querySelectorAll(config.multiclick);
        console.log('multiclickElements', multiclickElements);
        multiclickElements.forEach((element) => {
            element.click();
        });
    }
    repeatingElements = config.repeating_elements;
    var element = document.querySelector(config.elements.header);
    var imageElement = document.querySelector(config.elements.image);
    if (element) {
        console.log('element', element.textContent);
        var combined = element.textContent + '\n\n' + imageElement.src;
        console.log(imageElement.src);
        chrome.runtime.sendMessage({ action: "extract", text: combined });
    }
    if (repeatingElements.length != 0) {
        repeatingElements.forEach((elementConfig) => {
            var elements = document.querySelectorAll(elementConfig.selector);
            elements.forEach((element) => {
                console.log('element', element.textContent);
            });
        });
    }
});


chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
    if (request.action === "multiclick") {
        chrome.runtime.sendMessage({ action: "getConfig" }, function (response) {
            var config = response.config;
            if (config.multiclick && Array.isArray(config.multiclick)) {
                config.multiclick.forEach((selector) => {
                    var multiclickElements = document.querySelectorAll(selector);
                    multiclickElements.forEach((element) => {
                        element.click();
                    });
                });
            }
        });
    }
});
