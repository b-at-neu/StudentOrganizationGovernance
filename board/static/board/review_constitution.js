import { post } from "/static/post.js"

var htmlData

// #####################
//     On page load
// #####################

document.addEventListener("DOMContentLoaded", async () => {

    // Get HTML data
    htmlData = document.getElementById("data").dataset

    // Get data from server
    const { constitution: constitutionData } = await post(htmlData.getDataUrl, { "constitution_pk": htmlData.constitutionPk })
    const { constitution: oldConstitutionData } = 
        htmlData.oldConstitutionPk ? await post(htmlData.getDataUrl, { "constitution_pk": htmlData.oldConstitutionPk }) : { constitution: { articles: [] } }

    // Generate entire page
    generateArticles(constitutionData.articles, oldConstitutionData.articles)
    

})

// #####################
//    Text difference
// #####################

function getDifference(oldText, newText) {
    const subStrings = getSubstrings(oldText, newText)

    const span = document.createElement("span")

    // Creates html spans for substrings of specific types
    function createSubstringHTML(content, type) {
        if (content === "")
            return

        const subSpan = document.createElement("span")

        if (type === "old")
            subSpan.classList.add("old-content")
        else if (type === "new")
            subSpan.classList.add("new-content")

        subSpan.innerHTML = content
        span.appendChild(subSpan)
    }

    let i = 0, j = 0
    for (let subIndex = 0; subIndex < subStrings.length;) {
        let oldAtSub = (subStrings[subIndex].oldIndex == i)
        let newAtSub = (subStrings[subIndex].newIndex == j)

        if (oldAtSub && newAtSub) {
            // Handle substrings
            createSubstringHTML(subStrings[subIndex].substring, "normal")

            i += subStrings[subIndex].substring.length
            j += subStrings[subIndex].substring.length
            subIndex++ 

        } else if (!oldAtSub) {
            // Handle old strings
            createSubstringHTML(oldText.substring(i, subStrings[subIndex].oldIndex), "old")
            i = subStrings[subIndex].oldIndex

        } else if (!newAtSub) {
            // Handle new strings
            createSubstringHTML(newText.substring(j, subStrings[subIndex].newIndex), "new")
            j = subStrings[subIndex].newIndex
        } else {
            return "An error occured."
        }
    }


    // Handle old strings at end
    createSubstringHTML(oldText.substring(i), "old")

    // Handle new strings at end
    createSubstringHTML(newText.substring(j), "new")

    return span
}

function getSubstrings(oldStr, newStr) { 
    const subStrings = []
  
    for (let i = 0; i < oldStr.length; i++) { 
        for (let j = 0; j < newStr.length; j++) { 

            // Move j forwards to most recent substring
            if (j == 0 && subStrings.length > 0)
                j = subStrings[subStrings.length - 1].newIndex + subStrings[subStrings.length - 1].substring.length

            let substring = "", k = i, l = j
  
            while (k < oldStr.length &&  
                   l < newStr.length &&  
                   oldStr[k] === newStr[l]) {
                substring += oldStr[k] 
                                
                k++ 
                l++ 
            } 

            if (substring.length > 5) {
                subStrings.push({
                    substring,
                    oldIndex: i,
                    newIndex: j,
                })
                // Make sure not to check the same section again
                i = k
                j = l
            }
        }
    } 
    return subStrings; 
} 

// #####################
//  Create constitution
// #####################

function generateArticles(constitutionDataArticles, oldConstitutionDataArticles) {
    // Create each article
    let i = 0, j = 0
    while (i < constitutionDataArticles.length || j < oldConstitutionDataArticles.length) {
        
        if (
            i >= constitutionDataArticles.length || 
            (constitutionDataArticles[i].did != oldConstitutionDataArticles[j]?.did && oldConstitutionDataArticles.some(o => o?.did === constitutionDataArticles[i].did))
        ) {
            // Article deleted
            createArticle(oldConstitutionDataArticles[j].number, "", oldConstitutionDataArticles[j].title, oldConstitutionDataArticles[j].pk)
            generateSections([], oldConstitutionDataArticles[j].sections)
            j++
        } else if (j >= oldConstitutionDataArticles.length || constitutionDataArticles[i].did != oldConstitutionDataArticles[j]?.did) {
            // Article new
            createArticle(constitutionDataArticles[i].number, constitutionDataArticles[i].title, "", constitutionDataArticles[i].pk)
            generateSections(constitutionDataArticles[i].sections, [])
            i++
        } else {
            // Same article
            createArticle(constitutionDataArticles[i].number, constitutionDataArticles[i].title, oldConstitutionDataArticles[j].title, constitutionDataArticles[i].pk)
            generateSections(constitutionDataArticles[i].sections, oldConstitutionDataArticles[j].sections)
            i++, j++
        }
    }
}

function generateSections(constitutionDataSections, oldConstitutionDataSections) {

    // Create each section
    let k = 0, l = 0
    while (k < constitutionDataSections.length || l < oldConstitutionDataSections.length) {
            
        if (
            k >= constitutionDataSections.length || 
            (constitutionDataSections[k].did != oldConstitutionDataSections[l]?.did 
                && oldConstitutionDataSections.some(o => o?.did === constitutionDataSections[k].did))
        ) {
            // Section deleted
            createSection(
                oldConstitutionDataSections[l].number, "",
                oldConstitutionDataSections[l].content,
                oldConstitutionDataSections[l].pk
            )
            l++
        } else if (l >= oldConstitutionDataSections.length || constitutionDataSections.did != oldConstitutionDataSections.did) {
            // Section new
            createSection(
                constitutionDataSections[k].number,
                constitutionDataSections[k].content, "",
                constitutionDataSections[k].pk
            )
            k++
        } else {
            // Same section
            createSection(
                constitutionDataSections[k].number,
                constitutionDataSections[k].content,
                oldConstitutionDataSections[l].content,
                constitutionDataSections[k].pk
            )
            k++, l++
        }
    }
}

function createArticle(number, title, oldTitle, pk) {
    const table = document.querySelector("table#constitution")
    const tr = document.createElement("tr")

    // Number
    const th1 = document.createElement("th")
    if (title === "")
        th1.classList.add("old-content")
    else if (oldTitle === "")
        th1.classList.add("new-content")
    th1.innerHTML = "Article " + number
    tr.appendChild(th1)

    // Title
    const th2 = document.createElement("th")

    if (title === oldTitle)
        th2.innerHTML = title
    else
        th2.appendChild(getDifference(oldTitle, title))
    tr.appendChild(th2)

    // Button
    const th3 = document.createElement("th")
    const commentButton = document.createElement("button")
    commentButton.dataset.articlepk = pk
    commentButton.innerHTML = "Add Comment"
    //////////////////////////commentButton.addEventListener("click", () => addComment(commentButton))
    th3.appendChild(commentButton)
    tr.appendChild(th3)
    
    table.appendChild(tr)
}

function createSection(number, content, oldContent, pk) {
    const table = document.querySelector("table#constitution")
    const tr = document.createElement("tr")

    // Number
    const td1 = document.createElement("td")
    if (content === "")
        td1.classList.add("old-content")
    else if (oldContent === "")
        td1.classList.add("new-content")
    td1.innerHTML = "Section " + number
    tr.appendChild(td1)

    // Content
    const td2 = document.createElement("td")
    if (content === oldContent)
        td2.innerHTML = content
    else
        td2.appendChild(getDifference(oldContent, content))
    tr.appendChild(td2)

    // Button
    const td3 = document.createElement("td")
    const commentButton = document.createElement("button")
    commentButton.dataset.articlepk = pk
    commentButton.innerHTML = "Add Comment"
    //////////////////////////commentButton.addEventListener("click", () => addComment(commentButton))
    td3.appendChild(commentButton)
    tr.appendChild(td3)
    
    table.appendChild(tr)
}