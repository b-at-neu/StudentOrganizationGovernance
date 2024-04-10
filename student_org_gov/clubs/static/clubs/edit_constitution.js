import { post } from "/static/post.js"

var unsavedChanges
var htmlData

// #####################
//     On page load
// #####################

document.addEventListener("DOMContentLoaded", async () => {
    updateUnsavedChanges(false)

    // Get HTML data
    htmlData = document.getElementById("data").dataset
    
    // Get data from server
    const serverData = await post(htmlData.getDataUrl, { "constitution_pk": htmlData.constitutionPk })
    sessionStorage.setItem("constitution-data", JSON.stringify(serverData.constitution))

    // Generate entire page
    const data = JSON.parse(sessionStorage.getItem("constitution-data"))
    for (const article of data.articles) {
        createArticle(article.number, article.title, article.pk)
        for (const section of article.sections)
            createSection(section.number, section.content, section.pk, article.pk)
    }
    createAddArticleButton()

    // Update buttons and numbers
    updateButtonsAndNumbers()

    /* Create undo and redo storage
    sessionStorage.setItem("undo-data", JSON.stringify([]))
    sessionStorage.setItem("redo-data", JSON.stringify([]))

    // Add events to undo and redo buttons
    document.getElementById("undo").addEventListener("click", onUndo)
    document.getElementById("redo").addEventListener("click", onRedo)*/

    // Save data to DB on save button
    document.querySelector("button#save-edits").addEventListener("click", saveToDatabase)
            
    // Block leaving unsaved changes
    window.onbeforeunload = () => {
        if (unsavedChanges)
            return "You have unsaved changes"
    }
})



// #####################
//     On text edit
// #####################

function onArticleEdit(input) {
    updateUnsavedChanges(true)
    //createUndoPoint()

    // Update local data
    if (input.classList.contains("article"))
        updateLocalData((data) => 
            data.articles.find((o) => 
                o.pk == input.dataset.articlepk).title = input.value)
}

function onSectionEdit(textarea) {
    updateUnsavedChanges(true)
    //createUndoPoint()

    // Update local data
    if (textarea.classList.contains("section"))
        updateLocalData((data) => 
            data.articles.find((o) => 
                o.pk == textarea.dataset.articlepk).sections.find((o) => 
                    o.pk == textarea.dataset.sectionpk).content = textarea.value)
}



// #####################
//   On add or removal
// #####################

function onArticleRemoval(button) {

    // Ensure more than one article
    const data = JSON.parse(sessionStorage.getItem("constitution-data"))
    if (data.articles.length <= 1)
        return alert("Can not remove last article.")

    updateUnsavedChanges(true)
    //createUndoPoint()

    // Remove all rows
    document.querySelectorAll("tr.article-" + button.dataset.articlepk).forEach((i) => i.remove())

    // Update local data
    updateLocalData((data) => 
        data.articles.splice(data.articles.findIndex((o) => o.pk == button.dataset.articlepk), 1)
    )

    // Update buttons and numbers
    updateButtonsAndNumbers()
}

function onSectionRemoval(button) {

    // Ensure more than one section
    const data = JSON.parse(sessionStorage.getItem("constitution-data"))
    if (data.articles.find((o) => o.pk == button.dataset.articlepk).sections.length <= 1)
        return alert("Can not remove last section.")

    updateUnsavedChanges(true)
    //createUndoPoint()

    // Remove html
    button.parentNode.parentNode.remove()

    // Update local data
    updateLocalData((data) => {
        const array = data.articles.find((o) => o.pk == button.dataset.articlepk).sections
        array.splice(array.findIndex((o) => o.pk == button.dataset.sectionpk), 1)
    })

    // Update buttons and numbers
    updateButtonsAndNumbers()
}

async function onArticleAdd(button) {
    updateUnsavedChanges(true)
    //createUndoPoint()

    // Add to database
    const article = await post(htmlData.addArticleUrl, { "constitution": htmlData.constitutionPk })
    const section = await post(htmlData.addSectionUrl, { "article": article.pk })
    
    // Add html
    createArticle(article.number, "", article.pk)
    createSection(section.number, "", section.pk, article.pk)

    // Update local data
    updateLocalData((data) => data.articles.push({
        "number": article.number,
        "title": "",
        "pk": article.pk,
        "sections": [{
            "number": section.number,
            "content": "",
            "pk": section.pk
        }]
    }))

    // Update buttons and numbers
    updateButtonsAndNumbers()
}

async function onSectionAdd(button) {
    updateUnsavedChanges(true)
    //createUndoPoint()

    // Add to database
    const section = await post(htmlData.addSectionUrl, { "article": button.dataset.articlepk })
    
    // Add html
    createSection(section.number, "", section.pk, section.articlepk)

    // Update local data
    updateLocalData((data) => data.articles.find((o) => o.pk == button.dataset.articlepk).sections.push({
        "number": section.number,
        "content": "",
        "pk": section.pk
    }))

    // Update buttons and numbers
    updateButtonsAndNumbers()
}



// #####################
//      On save
// #####################

async function saveToDatabase() {
    updateUnsavedChanges(false)

    const data = JSON.parse(sessionStorage.getItem("constitution-data"))

    // Check for empty fields
    for (const article of data.articles) {
        if (article.title === "")
            return alert(`Unable to save. Article ${article.number} does not have a title.`)
        for (const section of article.sections) {
            if (section.content === "")
                return alert(`Unable to save. Article ${article.number} Section ${section.number} does not have any content.`)
        }
    }

    const result = await post(htmlData.saveEditsUrl, data)
    
    // Alert for errors
    if (result.result != "success")
        alert(result.errors)
}



// #####################
//        Undos
// #####################

/*function onUndo() {
    const currentData = JSON.parse(sessionStorage.getItem("constitution-data"))
    const undoData = JSON.parse(sessionStorage.getItem("undo-data"))
    const redoData = JSON.parse(sessionStorage.getItem("redo-data"))
    
    // Add current state to redo stack
    redoData.push(currentData)

    sessionStorage.setItem("constitution-data", JSON.stringify(undoData.pop()))
    sessionStorage.setItem("undo-data", JSON.stringify(undoData))
}


function onRedo() {

}


function createUndoPoint() {
    const currentData = JSON.parse(sessionStorage.getItem("constitution-data"))
    const undoData = JSON.parse(sessionStorage.getItem("undo-data"))

    // Append data
    undoData.push(currentData)

    sessionStorage.setItem("undo-data", JSON.stringify(undoData))
}*/




// #####################
//   Helper functions
// #####################

// Runs the function on the local data
function updateLocalData(func) {
    const data = JSON.parse(sessionStorage.getItem("constitution-data"))
    func(data)
    sessionStorage.setItem("constitution-data", JSON.stringify(data))
}


// Changes unsaved changes to a new state
function updateUnsavedChanges(state) {
    unsavedChanges = state

    // Change indicator text
    const indicator = document.querySelector("div#unsaved-changes-indicator")
    indicator.innerHTML = state ? "Unsaved Changes..." : "All changes saved!"
}


// Enables and disables buttons and renumbers
function updateButtonsAndNumbers() {
    const data = JSON.parse(sessionStorage.getItem("constitution-data"))

    // Article buttons
    const articleButtons = document.querySelectorAll("button.remove-article-button")

    if (data.articles.length <= 1)
        articleButtons.forEach((o) => o.disabled = true)
    else
        articleButtons.forEach((o) => o.disabled = false)
    
    // Section buttons
    for (const article of data.articles) {

        const sectionButtons = document.querySelectorAll("button.remove-section-button-article-" + article.pk)
        
        if (article.sections.length <= 1)
            sectionButtons.forEach((o) => o.disabled = true)
        else
            sectionButtons.forEach((o) => o.disabled = false)
    }

    const orderedArticles = data.articles.sort((a, b) => a.number - b.number)

    // Assign article numbers
    for (let i = 0; i < orderedArticles.length; i++) {
        orderedArticles[i].number = i + 1

        // Update html
        document.getElementById("article-number-" + orderedArticles[i].pk).innerHTML = "Article " + (i + 1)

        const orderedSections = orderedArticles[i].sections.sort((a, b) => a.number - b.number)

        // Assign section numbers
        for (let j = 0; j < orderedSections.length; j++) {

            // Update html
            document.getElementById("section-number-" + orderedSections[j].pk).innerHTML = "Section " + (j + 1)

            orderedSections[j].number = j + 1
        }
    }

    sessionStorage.setItem("constitution-data", JSON.stringify(data))
}



// #####################
//     Create html
// #####################

function createArticle(number, title, pk) {
    const table = document.querySelector("table#constitution")
    const insertRow = document.querySelector("tr#insert-articles")

    // Row 1 - Article
    const tr1 = document.createElement("tr")
    tr1.classList.add("article-" + pk)

    // Number
    const th1 = document.createElement("th")
    th1.id = "article-number-" + pk
    tr1.appendChild(th1)

    // Title
    const th2 = document.createElement("th")
    const titleInput = document.createElement("input")
    titleInput.classList.add("article")
    titleInput.dataset.articlepk = pk
    titleInput.type = "text"
    titleInput.value = title
    titleInput.style.width = "100%"
    titleInput.addEventListener("input", () => onArticleEdit(titleInput))
    th2.appendChild(titleInput)
    tr1.appendChild(th2)

    // Button
    const th3 = document.createElement("th")
    const removeButton = document.createElement("button")
    removeButton.classList.add("remove-article-button")
    removeButton.dataset.articlepk = pk
    removeButton.innerHTML = "Remove Article"
    removeButton.addEventListener("click", () => onArticleRemoval(removeButton))
    th3.appendChild(removeButton)
    tr1.appendChild(th3)

    // Row 2 - placeholder
    const tr2 = document.createElement("tr")
    tr2.classList.add("article-" + pk)
    tr2.id = "insert-article-" + pk

    // Row 3 - add section button
    const tr3 = document.createElement("tr")
    tr3.classList.add("article-" + pk)

    // Empty
    tr3.appendChild(document.createElement("td"))

    // Button
    const td = document.createElement("td")
    const addButton = document.createElement("button")
    addButton.dataset.articlepk = pk
    addButton.innerHTML = "Add Section"
    addButton.addEventListener("click", async () => onSectionAdd(addButton))
    td.appendChild(addButton)
    tr3.appendChild(td)

    // Empty
    tr3.appendChild(document.createElement("td"))
    
    table.insertBefore(tr1, insertRow)
    table.insertBefore(tr2, insertRow)
    table.insertBefore(tr3, insertRow)
}


function createSection(number, content, pk, article_pk) {
    const table = document.querySelector("table#constitution")
    const insertRow = document.querySelector("tr#insert-article-" + article_pk)
    
    // Row
    const tr = document.createElement("tr")
    tr.classList.add("article-" + article_pk)

    // Number
    const td1 = document.createElement("td")
    td1.id = "section-number-" + pk
    tr.appendChild(td1)

    // Title
    const td2 = document.createElement("td")
    const contentTextArea = document.createElement("textarea")
    contentTextArea.classList.add("section")
    contentTextArea.dataset.articlepk = article_pk
    contentTextArea.dataset.sectionpk = pk
    contentTextArea.rows = 10
    contentTextArea.style.resize = "vertical"
    contentTextArea.style.width = "100%"
    contentTextArea.innerHTML = content
    contentTextArea.addEventListener("input", () => onSectionEdit(contentTextArea))
    td2.appendChild(contentTextArea)
    tr.appendChild(td2)

    // Button
    const td3 = document.createElement("td")
    const removeButton = document.createElement("button")
    removeButton.classList.add("remove-section-button-article-" + article_pk)
    removeButton.dataset.articlepk = article_pk
    removeButton.dataset.sectionpk = pk
    removeButton.innerHTML = "Remove Section"
    removeButton.addEventListener("click", () => onSectionRemoval(removeButton))
    td3.appendChild(removeButton)
    tr.appendChild(td3)

    table.insertBefore(tr, insertRow)
}


function createAddArticleButton() {
    const table = document.querySelector("table#constitution")

    // Insert row
    const insertRow = document.createElement("tr")
    insertRow.id = "insert-articles"
    table.appendChild(insertRow)

    // Row
    const tr = document.createElement("tr")

    tr.appendChild(document.createElement("td"))

    // Button
    const td = document.createElement("td")
    const addButton = document.createElement("button")
    addButton.classList.add("add-article")
    addButton.addEventListener("click", async () => onArticleAdd(addButton))
    addButton.innerHTML = "Add Article"
    td.appendChild(addButton)
    tr.appendChild(td)

    tr.appendChild(document.createElement("td"))

    table.appendChild(tr)
}