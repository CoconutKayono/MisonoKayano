function populateLanguageSwitcher(data, currentLang) {
  if (data.length <= 1) // <= 1 set of docs exist for this package so return
    return;

  const pathSub = /^.*?\/Packages/;
  const baseUrl = location.pathname.replace(pathSub, "/Packages");
  const shortVersion = getShortVersion(thisPackageMetaData.version);
  const languageSwitcher = ["<div id='language-switcher'>", "<label for='language-select'>Language: <select id='language-select'>", "</select></label>", "</div>"];
  
  // Create the language selector
  $('#breadcrumb').append($(languageSwitcher.join("\n")));

  const $languageSelect = $("#language-select");

  // Populate the language selector
  for (let i = 0; i < data.length; i++) {
    const element = data[i];
    const lang = element.lang;
    const langUrlPrefix = element.pathPrefix;
    const className = `language-switcher-language-${lang}`;
    let targetUrl = "";
    let selectedOption = "";

    if (langUrlPrefix.length > 0)
      targetUrl = `/${langUrlPrefix}`;

    if (element.lang === currentLang || (element.lang === 'en' && !currentLang))
      selectedOption = "selected";

    if (element.versions.includes(shortVersion)) {
      // If the same version exists for the other language, send to same pagePath
      targetUrl += baseUrl;
    }
    else {
      // Else send to latest because another version exists
      targetUrl += `/${!isOffline ? "Packages/" : ""}${thisPackageMetaData.name}@${getLatestVersion(element.versions)}/index.html`;
    }

    $languageSelect.append(`<option class="${className}" value="${targetUrl}" ${selectedOption}>${element.display}</li>`);
  }

  $languageSelect.change(function () {
    location.href = $(this).val();
  });

  localStorage.setItem("docs-lang", currentLang);
}

function getShortVersion(longVersion) {
  const longVersSplit = longVersion.split('.');
  return `${longVersSplit[0]}.${longVersSplit[1]}`;
}

function getLatestVersion(versions) {
  const sortedVersions = versions.sort(stringShortVersionComparator);
  return sortedVersions[0];
}

function stringShortVersionComparator(a, b) {
  const aSplit = a.split(".");
  const bSplit = b.split(".");

  const aMajor = parseInt(aSplit[0]);
  const bMajor = parseInt(bSplit[0]);

  if (isNaN(aMajor) || isNaN(bMajor))
    return 0;

  if (aMajor > bMajor)
    return -1;
  if (bMajor > aMajor)
    return 1;
  
  const aMinor = parseInt(aSplit[1]);
  const bMinor = parseInt(bSplit[1]);

  if (isNaN(aMinor) || isNaN(bMinor))
    return 0;

  if (aMinor > bMinor)
    return -1;
  if (bMinor > aMinor)
    return 1;

  return 0;
}
