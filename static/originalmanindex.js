
// Initial References: Credit to Coding Artist with the starter pack/beginner version of this game https://www.youtube.com/watch?v=T6uht1A0114
const letterContainer = document.getElementById("letter-gamecontainer");
const optionsContainer = document.getElementById("options-gamecontainer");
const userInputSection = document.getElementById("user-input-section");
const newGameContainer = document.getElementById("new-game-container");
const newGameButton = document.getElementById("new-game-button");
const canvas = document.getElementById("canvas");
const resultText = document.getElementById("result-text");

// Options values for buttons
let options = {
    Miijim: [
        "Miishimin",
        "Miin",
        "Wezaawiminagizid",
        "Miskomin",
        "Manoomin",
        "Eshkandaming",
        "Doodooshaaboo",
        "Zaawaamide",
    ],
    Foods: [
        "Apple",
        "Blueberry",
        "Orange",
        "Raspberry",
        "Rice",
        "Watermelon",
        "Bread",
        "Butter",
    ],
    Clans: [
        "Crane",
        "Loon",
        "Bear",
        "Fish",
        "Deer",
        "Eagle",
        "Wolf",
        "Turtle",
    ],
    Dodems: [
        "Ajijaak",
        "Maang",
        "Makwa",
        "Giigoonh",
        "Waawaashkeshi",
        "Migizi",
        "Maiingan",
        "Mikinaak",
    ],
};

// Count
let winCount = 0;
let count = 0;

// Hide word
let chosenWord = "";

// Display options on screen
const displayOptions = () => {
    optionsContainer.innerHTML += `<h3>Please select an Option</h3>`;
    let buttonCon = document.createElement("div");
    for (let value in options) {
        buttonCon.innerHTML += `<button class="options" onclick="generateWord('${value}')">${value}</button>`;
    }
    optionsContainer.appendChild(buttonCon);
};

// Block all the buttons
const blocker = () => {
    let optionsButtons = document.querySelectorAll(".options");
    let letterButtons = document.querySelectorAll(".letters");

    // Disable all options
    optionsButtons.forEach((button) => {
        button.disabled = true;
    });

    // Disable all letters
    letterButtons.forEach(button => {
        button.disabled.true;
    });
    newGameContainer.classList.remove("hide");
};

// Word generator
const generateWord = (optionValue) => {
    let optionsButtons = document.querySelectorAll(".options");

    // If optionValue matches the button innerText then highlight the button
    optionsButtons.forEach((button) => {
        if (button.innerText.toLowerCase() === optionValue) {
            button.classList.add("active");
        }
        button.disabled = true;
    });

    // Initially hide letter, clear previous word
    letterContainer.classList.remove("hide");
    userInputSection.innerText = "";

    let optionArray = options[optionValue];

    // Chose random word
    chosenWord = optionArray[Math.floor(Math.random() * optionArray.length)];
    chosenWord = chosenWord.toUpperCase();
    console.log(chosenWord);

    let displayItem = chosenWord.replace(/./g, '<span class="dashes">_</span>');

    // Display each element as span
    userInputSection.innerHTML = displayItem;
};

// Initial Function (called when page loads/user presses new game)
const initializer = () => {
    winCount = 0;
    count = 0;

    // Initially erase all content, and hide letters and new game button
    userInputSection.innerHTML = "";
    optionsContainer.innerHTML = "";
    letterContainer.classList.add("hide");
    newGameContainer.classList.add("hide");
    letterContainer.innerHTML = "";

    // For creating letter buttons
    for (let i = 65; i < 91; i++) {
        let button = document.createElement("button");
        button.classList.add("letter");
        // Numbers to ASCII A-Z
        button.innerText = String.fromCharCode(i);
        // Char button click
        button.addEventListener("click", () => {
            let charArray = chosenWord.split("");
            let dashes = document.getElementsByClassName("dashes");
            // If array contains the clicked value, replace the matched dash with letter
            if (charArray.includes(button.innerText)) {
                charArray.forEach((char, index) => {
                    // If Char in array is same as clicked button
                    if (char === button.innerText) {
                        // Replace dash with letter
                        dashes[index].innerText = char;
                        // Increment counter
                        winCount += 1;
                        // If wordCount equals word length
                        if (winCount == charArray.length) {
                            resultText.innerHTML = `<h2 class='win-msg'>You Win!!</h2><p>The word was <span>${chosenWord}</span></p>`;
                            // Block all buttons
                            blocker();
                        }
                    }
                });
            }
            else {
                // lose count
                count += 1;
                // For drawing man
                drawMan(count);
                // Count == 6 because 1-head, 2-body, 3-left arm, 4-right arm, 5-left leg, 6-right leg
                if (count == 7) {
                    resultText.innerHTML = `<h2 class='lose-msg'>You lose...</h2><p>The word was <span>${chosenWord}</span></p>`;
                    // Block all buttons
                    blocker();
                }
            }
            // Disable clicked button
            button.disabled = true;
        });
        letterContainer.append(button);
    }

    displayOptions();

    // Call to canvas creator (for clearing prev canvases or creatin inital canvas)
    let { initialDrawing } = canvasCreator();
    // Inital drawing would draw the frame
    initialDrawing();
};

// Canvas
const canvasCreator = () => {
    let context = canvas.getContext("2d");
    context.beginPath();
    context.strokeStyle = "#000";
    context.lineWidth = 2;

    // For drawing lines
    const drawLine = (fromX, fromY, toX, toY) => {
        context.moveTo(fromX, fromY);
        context.lineTo(toX, toY);
        context.stroke();
    };

    const head = () => {
        context.beginPath();
        context.arc(150, 30, 10, 0, Math.PI * 2, true);
        context.stroke();
    };

    const body = () => {
        drawLine(150, 40, 150, 80);
    };

    const rightArm = () => {
        drawLine(150, 60, 125, 50);
    };

    const leftArm = () => {
        drawLine(150, 60, 175, 50);
    };

    const rightLeg = () => {
        drawLine(150, 80, 130, 120);
    };

    const leftLeg = () => {
        drawLine(150, 80, 170, 120);
    };

    const hat = () => {
        drawLine(140, 80, 50, 110);
    };


    // Initial Frame
    const initialDrawing = () => {
        // Clear Canvas
        context.clearRect(0, 0, context.canvas.width, context.canvas.height);

        context.beginPath();
        context.arc(150, 298, 180, 0, Math.PI * 2, true);
        context.stroke();
        context.fillStyle = "OliveDrab";
        context.fill();

        context.beginPath();
        context.arc(265, 150, 12, 0, Math.PI * 2, true);
        context.stroke();
        context.fillStyle = "peru";
        context.fill();

        context.beginPath();
        context.moveTo(35,150);
        context.lineTo(35,140);
        context.lineTo(50,150);
        context.fillStyle = "peru";
        context.fill();

        drawLine(275, 144, 100, 280);
        drawLine(262, 143, 265, 144);
    };

    return { initialDrawing, head, body, rightArm, leftArm, rightLeg, leftLeg, hat };
};

// Draw the man
const drawMan = (count) => {
    let { head, body, rightArm, leftArm, rightLeg, leftLeg, hat } = canvasCreator();
    switch (count) {
        case 1:
            head();
            break;
        case 2:
            body();
            break;
        case 3:
            rightArm();
            break;
        case 4:
            leftArm();
            break;
        case 5:
            rightLeg();
            break;
        case 6:
            leftLeg();
            break;
        case 7:
            hat();
            break;
        default:
            break;
    }
};

// New Game
newGameButton.addEventListener("click", initializer);
window.onload = initializer;