const isOffline = !location.host || (location.host.indexOf('unity3d.com') === -1 && location.host.indexOf('unity.com') === -1);

$(function(){
    if (isOffline) {
        onLastPopulate();
        return;
    }
    
    const pathLanguageRegex = /^\/(?:(?<lang>.*?)\/)?Packages\//;
    const pathLanguageMatch = location.pathname.match(pathLanguageRegex);

    let languageMatch;
    if (!isOffline)
        languageMatch = pathLanguageMatch.groups.lang;
    else
        languageMatch = thisPackageMetaData.lang;

    const packageName = thisPackageMetaData.name;
    const urlPrefix = !isOffline ? '/Packages' : '';

    let hasPopulated = false;

    function getPackageMetaData(callback){
        const requestURL = `${urlPrefix}/metadata/${packageName}/metadata.json`;
        
        request(requestURL, callback);
    }

    function getSwitcherData(callback) {
        const requestURL = `${urlPrefix}/metadata/${packageName}/versions.json`;

        request(requestURL, callback);
    }

    function request(requestURL, callback){
        if (!hasPopulated){
            $.getJSON(requestURL, function(data){
                callback(data);
            }).fail(function(){
                callback();
            });
        }
    }    
    
    getSwitcherData(function(versionsData) {
        if (!versionsData || !versionsData.langs) {
            // No data for lang switcher
            onLastPopulate();
            return;
        }

        populateLanguageSwitcher(versionsData.langs, languageMatch); // See language-switcher.js

        getPackageMetaData(function(metadata){
            populateVersionSwitcher(metadata, versionsData.langs, languageMatch); // See version-switcher.js
        });
    });
});