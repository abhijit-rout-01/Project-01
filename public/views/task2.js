let canvas, ctx, pS=5, currentImg, img, drawing = false, startX, startY;
const images = [
    '/css/task2/background.jpeg',
    '/css/task2/background.jpeg',
    '/css/task2/background.jpeg', // Add more images as needed
];
let currentIndex = 0;
let history = []; // Array to store history of canvas states

function openEditor(container) {
    const editor = document.getElementById('editor');
    canvas = document.getElementById('canvas');
    ctx = canvas.getContext('2d');
    img = container.querySelector('img');
    currentImg = container;

    // Resize canvas to fit the screen while maintaining aspect ratio
    const aspectRatio = img.naturalWidth / img.naturalHeight;
    if (window.innerWidth / window.innerHeight > aspectRatio) {
        canvas.height = window.innerHeight;
        canvas.width = window.innerHeight * aspectRatio;
    } else {
        canvas.width = window.innerWidth;
        canvas.height = window.innerWidth / aspectRatio;
    }

    ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
    editor.style.display = 'block';

    // Save initial state
    saveState();

    canvas.addEventListener('mousedown', startDrawing);
    canvas.addEventListener('mousemove', draw);
    canvas.addEventListener('mouseup', stopDrawing);
    canvas.addEventListener('mouseout', stopDrawing);
}

function closeEditor() {
    const editor = document.getElementById('editor');
    editor.style.display = 'none';
    canvas.removeEventListener('mousedown', startDrawing);
    canvas.removeEventListener('mousemove', draw);
    canvas.removeEventListener('mouseup', stopDrawing);
    canvas.removeEventListener('mouseout', stopDrawing);
}

function startDrawing(e) {
    drawing = true;
    ctx.beginPath();
    ctx.moveTo(e.offsetX, e.offsetY);
}

function draw(e) {
    if (!drawing) return;

    ctx.lineTo(e.offsetX, e.offsetY);
    ctx.strokeStyle = 'black';
    ctx.lineWidth = pS; // Increased line width
    ctx.stroke();

    //console.log(pS);
}

function penSize(){
    pS = document.getElementById('penSize').innerHTML;
    pS = (parseInt(pS)*2)%35;
    ctx.lineWidth = pS; 
    document.getElementById('penSize').innerHTML = ctx.lineWidth;
    console.log(pS);
}

function stopDrawing() {
    drawing = false;
    ctx.closePath();
    saveState(); // Save the state after drawing
}

function saveState() {
    history.push(canvas.toDataURL());
}

function undoDrawing() {
    if (history.length > 1) {
        history.pop(); // Remove the current state
        const previousState = history[history.length - 1];
        const img = new Image();
        img.src = previousState;
        img.onload = () => {
            ctx.clearRect(0, 0, canvas.width, canvas.height); // Clear the canvas
            ctx.drawImage(img, 0, 0); // Restore the previous state
        };
    }
}

async function saveImage() {
    //save
    let img = currentImg.querySelector('img');
    const link = document.createElement('a');
    link.href = canvas.toDataURL('image/jpeg');
    link.download = 'edited-image.jpeg';
    link.click();

    await fetch(canvas.toDataURL('image/jpeg'))
    .then(response => response.blob())
    .then(blob => {
        const formData = new FormData();
        formData.append('image', blob, (img.src).substring(21));

        return fetch('/upload', {
            method: 'POST',
            body: formData
        });
    })
    .then(response => {
        if (response.ok) {
            console.log('Image uploaded successfully.');
        } else {
            console.error('Failed to upload image.');
        }
    })
    .catch(error => console.error('Error:', error));

    // Replace the current image with the next one in the list
    // currentIndex = (currentIndex + 1) % images.length;
    // currentImg.querySelector('img').src = images[currentIndex];
    closeEditor();
    removeImageJson(img);
    //reload();
}

function removeImageJson(img){
    //console.log(src);
    // Fetch the JSON file
    let src = img.src;
    src_new="";
    for(var i=src.length-1;i>=0;i--){
        if(src[i]==='/'){
            break;
        }
    }
    src = '/images'+src.substring(i);
    //console.log(src==images[0]);
    fetch('/css/task2/images.json')
        .then(response => response.json())
        .then(images => {
            //console.log("Original JSON data:", images);

            // Find the index of the image to remove
            const index = images.indexOf(src);
            console.log(src);
            //console.log(src===images[0]);
            if (index !== -1) {
                // Remove the element from the array
                images.splice(index, 1);

                //console.log("Updated JSON data after removal:", images);

                // Optionally, save the updated JSON back to the server
                // (This requires server-side handling, which isn't covered here)
                let updateResponse = fetch('update-json', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(images),
                });
    
                if (updateResponse.ok) {
                    console.log(images);
                } else {
                    //console.log("Failed to save updated JSON file.");
                }
            } else {
                console.log("Image not found in JSON data.");
            }
        })
        .catch(error => console.error('Error loading JSON:', error));
}

