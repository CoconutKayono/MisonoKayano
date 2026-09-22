const packagePathRegex = /.*?(?:@|(?:%40)).*?\/(?<path>.*)/;
const pagePath = location.pathname.match(packagePathRegex).groups.path;

let versionsAdded = 0;
let versionsToAdd = [];

const versionSwitcherHtml = `
<div id="version-switcher-select">
    <div class="component-select">
        <div id="component-select-current-display" class="component-select__current">
        ${thisPackageMetaData.displayTitle}
        </div>
        <ul id="version-switcher-ul" class="component-select__options-container">
        </ul>
    </div>
</div>
`;

function populateVersionSwitcher(metadata, versionsData, currentLang){
    $('#breadcrumb').append($(versionSwitcherHtml)); // Create version switcher select box
    let versionsToPopulate = {};
    let numberToPopulate = 0;
    let populatedCounter = 0;
    
    let orderedMetadataKeys;
    if (metadata)
        orderedMetadataKeys = Object.keys(metadata.versions).sort(packageVersionComparator);

    let thisVersionInfo;
    let enVersionInfo;
    for (let i = 0; i < versionsData.length; ++i) {
        if (versionsData[i].lang === "en")
            enVersionInfo = versionsData[i];
        if ((!currentLang && versionsData[i].lang === 'en') || currentLang === versionsData[i].lang)
            thisVersionInfo = versionsData[i];
    }
    
    for (let i = 0; i < enVersionInfo.versions.length; ++i) {
        const version = enVersionInfo.versions[i];
        const thisPackageVersionShort = getShortVersion(thisPackageMetaData.version);
        if (thisPackageVersionShort === version)
            continue;

        const isLocalised = thisVersionInfo.versions.includes(version);
        let unityVersion;
        if (metadata)
            unityVersion = getUnityVersionFromShortVersion(version, metadata.versions, orderedMetadataKeys);
        versionsToPopulate[version] = { unityVersion, isLocalised }
        ++numberToPopulate;
    }

    if (numberToPopulate <= 0)
    {
        onLastPopulate();
        return;
    }

    for (const version in versionsToPopulate){
        const baseGotoUrl = getRedirectUrl(version, versionsToPopulate[version].isLocalised, currentLang);
        const exactGotoUrl = `${baseGotoUrl}${pagePath}`;

        $.ajax( exactGotoUrl )
        .done(function() {
            addToList(version, exactGotoUrl, versionsToPopulate[version].unityVersion);
            versionsAdded++;
            if (++populatedCounter >= numberToPopulate){
                onLastPopulate();
            }
        })
        .fail(function() {
            addToList(version, baseGotoUrl, versionsToPopulate[version].unityVersion);
            versionsAdded++;

            if (++populatedCounter >= numberToPopulate){
                onLastPopulate();
            }
        });
    }
}

function getUnityVersionFromShortVersion(shortVersion, versionsInfo, orderedMetadataKeys) {
    for (let i = 0; i < orderedMetadataKeys.length; ++i) {
        const version = orderedMetadataKeys[i];
        const versionAsShort = getShortVersion(version);

        if (versionAsShort === shortVersion) {
            let unityVersion = "";
            if(versionsInfo[version].unity)
                unityVersion += versionsInfo[version].unity;
            if(versionsInfo[version].unityRelease)
                unityVersion += "." + versionsInfo[version].unityRelease;
            return unityVersion;
        }
    }

    return "";
}


function packageVersionComparator(a, b) {
    const aSplit = a.split('.');
    const bSplit = b.split('.');

    for (let i = 0; i < aSplit.length; i++) {
        const aPreviewSplit = aSplit[i].split('-');
        const bPreviewSplit = bSplit[i].split('-');

        if (aPreviewSplit.length !== bPreviewSplit.length)
            return getNormalizedComparisonValue(bPreviewSplit.length, aPreviewSplit.length);

        if (aPreviewSplit.length > 1) {
            const parsedA = parseInt(aPreviewSplit[0]);
            const parsedB = parseInt(bPreviewSplit[0]);

            if (parsedA === parsedB)
                return 0; // No point in further comparison as likely no change in compatible unity version between patch versions of the package
            else
                return getNormalizedComparisonValue(parsedA, parsedB);
                
        }

        const parsedA = parseInt(aSplit[i]);
        const parsedB = parseInt(bSplit[i]);

        if (parsedA !== parsedB)
            return getNormalizedComparisonValue(parsedA, parsedB);
    }
}

function getNormalizedComparisonValue(lhs, rhs) {
    if (lhs > rhs)
        return -1;
    if (rhs > lhs)
        return 1;
    return 0;
}

function getShortVersion(version) {
    const versionSplit = version.split('.');
    return `${versionSplit[0]}.${versionSplit[1]}`;
}

function onLastPopulate(){
    if (versionsAdded <= 0){
        $('#version-switcher-select').remove();
        $('#breadcrumb').append($('<p style="margin: 10px 0;"><b>' + thisPackageMetaData.displayTitle + '</b></p>'));
    }
    else {
        versionsToAdd = versionsToAdd.sort( 
            (a, b) => -a.version.localeCompare(b.version, "en-US", { numeric:true }) 
        );

        for (var i = 0; i < versionsToAdd.length; i++){
            createVersionOption(versionsToAdd[i].version, versionsToAdd[i].gotoUrl, versionsToAdd[i].unityVersion);
        }

        onVersionSwitcherClick();
    }
}

function addToList(version, gotoUrl, unityVersion){
    versionsToAdd.push({version:version, gotoUrl:gotoUrl, unityVersion:unityVersion});
    ++versionsAdded;
}

function createVersionOption(version, gotoUrl, unityVersion){
    let item ="";
    if(unityVersion)
        item = $(`<a style="color:#000;" href="${gotoUrl}"><li class="component-select__option" style='justify-content:space-between;'>${version} <span style="color:#aaa;">${unityVersion}+</span></li></a>`);
    else
        item = $(`<a style="color:#000;" href="${gotoUrl}"><li class="component-select__option">${version}</li></a>`);
    $('#version-switcher-ul').append(item);
}

function getRedirectUrl(versionTrimmed, isLocalised, currentLang){
    let output = `/Packages/${thisPackageMetaData.name}@${versionTrimmed}/`;
    if (isLocalised && currentLang && currentLang !== 'en')
        output = `/${currentLang}${output}`;
    return output;
}

function onVersionSwitcherClick(){
    $('#component-select-current-display').click(function(){
        $('#component-select-current-display').toggleClass('component-select__current--is-active');
    });
}

$(document).click(function(e){
    if (!(e.target.id == 'component-select-current-display'))
        $('#component-select-current-display').removeClass('component-select__current--is-active');
});