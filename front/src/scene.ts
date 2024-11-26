import GUI from "lil-gui";
import {
    AmbientLight,
    Group,
    LoadingManager,
    Mesh,
    MeshStandardMaterial,
    PCFSoftShadowMap,
    PerspectiveCamera,
    PointLight,
    Raycaster,
    Scene,
    Vector2,
    WebGLRenderer,
} from "three";
import { DragControls } from "three/examples/jsm/controls/DragControls";
import { TrackballControls } from "three/examples/jsm/controls/TrackballControls";
// import Stats from "three/examples/jsm/libs/stats.module";
import { resizeRendererToDisplaySize } from "./helpers/responsiveness";
import { Rubik } from "./rubik";
import "./style.css";

const CANVAS_ID = "scene";

let canvas: HTMLElement;
let renderer: WebGLRenderer;
let scene: Scene;
let loadingManager: LoadingManager;
let ambientLight: AmbientLight;
let pointLight: PointLight;
let rubikCubeMesh: Mesh;
let rubikCube: Rubik;
export let camera: PerspectiveCamera;
let cameraControls: TrackballControls;
let dragControls: DragControls;
// let stats: Stats;
// let gui: GUI;
const shuffleButton: any = document.getElementById("shuffle");
const solveButton: any = document.getElementById("solve");
const solveInfinite: any = document.getElementById("infinite");
const animation = { enabled: true, play: true };

const raycaster = new Raycaster();
const mouse = new Vector2();

export const movements = document.getElementById("moves-text");

export let stepList = [];
export const solveMoves = document.getElementById("solve-moves");

let raycasteable: Array<Group> = new Array<Group>();
let shiftPressed: boolean = false;

export let cantSentinelas = 3;

start();
update();

function start() {
    solveMoves!.style.display = "none";

    shuffleButton.addEventListener("click", () => {
        stepList = [];
        rubikCube.shuffle();
    });

    solveInfinite.addEventListener("click", () => {
        const span = document.createElement('span');
        span.className = 'hito';
        span.textContent = 'Resolviendo...';
        movements.insertBefore(span, movements.firstChild);

        let moves = rubikCube.applyedMoves.join(",");
        moves = moves + ",";
        moves = moves.substring(0, moves.length - 1);
        let url = "http://localhost:8000/resolve/" + moves;
        fetch(url, { method: "GET" })
            .then((response) => response.json())
            .then((json) => {
                rubikCube.resolveMovements = 0;
                solveMoves!.style.display = "none";
                let steps = json.resolve;
                steps = steps.endsWith(",")
                    ? steps.substring(0, steps.length - 1)
                    : steps;
                stepList = steps.split(",");
                solveMoves!.style.display = "block";
                solveMoves!.innerHTML = "(0 / " + (stepList.length - cantSentinelas) + ")";

                stepList.forEach((step: string) => {
                    rubikCube.applyMoves(step);
                    if (step === "|Cubo resuelto"){
                        setTimeout(() => {
                            rubikCube.reset();
                        }, rubikCube.moveQueue.length * rubikCube.rotationTime + 5000);
                    }
                });
            });
    });

    solveButton.addEventListener("click", () => {
        //TODO CAMBIAR ↓

        const span = document.createElement('span');
        span.className = 'hito';
        span.textContent = 'Resolviendo...';
        movements.insertBefore(span, movements.firstChild);

        let moves = rubikCube.applyedMoves.join(",");
        moves = moves + ",";
        moves = moves.substring(0, moves.length - 1);
        let url = "http://localhost:8000/resolve/" + moves;
        fetch(url, { method: "GET" })
            .then((response) => response.json())
            .then((json) => {
                rubikCube.resolveMovements = 0;
                solveMoves!.style.display = "none";
                let steps = json.resolve;
                steps = steps.endsWith(",")
                    ? steps.substring(0, steps.length - 1)
                    : steps;
                stepList = steps.split(",");
                solveMoves!.style.display = "block";
                solveMoves!.innerHTML = "(0 / " + (stepList.length - cantSentinelas) + ")";

                stepList.forEach((step: string) => {                    
                    rubikCube.applyMoves(step);
                });
            });
    });

    canvas = document.querySelector(`canvas#${CANVAS_ID}`)!;
    renderer = new WebGLRenderer({ canvas, antialias: true, alpha: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = PCFSoftShadowMap;
    scene = new Scene();

    loadingManager = new LoadingManager();

    loadingManager.onStart = () => {
        console.log("loading started");
    };
    loadingManager.onProgress = (url, loaded, total) => {
        console.log("loading in progress:");
        console.log(`${url} -> ${loaded} / ${total}`);
    };
    loadingManager.onLoad = () => {
        console.log("loaded!");
    };
    loadingManager.onError = () => {
        console.log("❌ error while loading");
    };

    pointLight = new PointLight("white", 50, 100);
    pointLight.position.set(2, 4, 2);
    pointLight.castShadow = true;
    pointLight.shadow.radius = 4;
    pointLight.shadow.camera.near = 0.5;
    pointLight.shadow.camera.far = 4000;
    pointLight.shadow.mapSize.width = 16;
    pointLight.shadow.mapSize.height = 16;

    ambientLight = new AmbientLight("white", 2);

    scene.add(pointLight);
    scene.add(ambientLight);

    rubikCube = new Rubik(2, 2, 2, 50);
    scene.add(rubikCube.getCube());
    rubikCubeMesh = rubikCube.getCentralMesh();

    camera = new PerspectiveCamera(
        50,
        canvas.clientWidth / canvas.clientHeight,
        0.1,
        100
    );
    camera.position.set(
        rubikCube.getX() * 4,
        rubikCube.getY() * 3,
        rubikCube.getZ() * 4
    );

    cameraControls = new TrackballControls(camera, canvas);
    cameraControls.target = rubikCubeMesh.position.clone();
    cameraControls.rotateSpeed = 5.0;
    cameraControls.zoomSpeed = 0.2;
    cameraControls.panSpeed = 2;
    cameraControls.update();

    dragControls = new DragControls(
        [rubikCubeMesh],
        camera,
        renderer.domElement
    );
    dragControls.addEventListener("hoveron", (event) => {
        const mesh = event.object as Mesh;
        const material = mesh.material as MeshStandardMaterial;
        material.emissive.set("orange");
    });
    dragControls.addEventListener("hoveroff", (event) => {
        const mesh = event.object as Mesh;
        const material = mesh.material as MeshStandardMaterial;
        material.emissive.set("black");
    });
    dragControls.addEventListener("dragstart", (event) => {
        const mesh = event.object as Mesh;
        const material = mesh.material as MeshStandardMaterial;
        cameraControls.enabled = false;
        animation.play = false;
        material.emissive.set("black");
        material.opacity = 0.7;
        material.needsUpdate = true;
    });
    dragControls.addEventListener("dragend", (event) => {
        cameraControls.enabled = true;
        animation.play = true;
        const mesh = event.object as Mesh;
        const material = mesh.material as MeshStandardMaterial;
        material.emissive.set("black");
        material.opacity = 1;
        material.needsUpdate = true;
    });
    dragControls.enabled = false;

    // stats = new Stats();
    // stats.dom.classList.add("stats-bottom-right");
    // document.body.appendChild(stats.dom);

    // gui = new GUI({ title: "🐞 Debug GUI", width: 300 });
    //
    // const RubikCubeFolder = gui.addFolder("Rubik Cube");
    //
    // RubikCubeFolder.add(rubikCube, "rotateU").name("rotate U");
    // RubikCubeFolder.add(rubikCube, "rotateUPrime").name("rotate U'");
    // RubikCubeFolder.add(rubikCube, "rotateR").name("rotate R");
    // RubikCubeFolder.add(rubikCube, "rotateRPrime").name("rotate R'");
    // RubikCubeFolder.add(rubikCube, "rotateF").name("rotate F");
    // RubikCubeFolder.add(rubikCube, "rotateFPrime").name("rotate F'");
    // RubikCubeFolder.add(rubikCube, "rotateD").name("rotate D");
    // RubikCubeFolder.add(rubikCube, "rotateDPrime").name("rotate D'");
    // RubikCubeFolder.add(rubikCube, "rotateL").name("rotate L");
    // RubikCubeFolder.add(rubikCube, "rotateLPrime").name("rotate L'");
    // RubikCubeFolder.add(rubikCube, "rotateB").name("rotate B");
    // RubikCubeFolder.add(rubikCube, "rotateBPrime").name("rotate B'");
    // RubikCubeFolder.add(rubikCube, "shuffle").name("shuffle");
    //
    // // persist GUI state in local storage on changes
    // gui.onFinishChange(() => {
    //     const guiState = gui.save();
    //     localStorage.setItem("guiState", JSON.stringify(guiState));
    // });

    // load GUI state if available in local storage
    // const guiState = localStorage.getItem("guiState");
    // if (guiState) gui.load(JSON.parse(guiState));

    // reset GUI state button
    // const resetGui = () => {
    //     localStorage.removeItem("guiState");
    //     gui.reset();
    //     window.location.reload();
    // };
    // gui.add({ resetGui }, "resetGui").name("RESET");
    //
    // gui.close();

    window.addEventListener("mousemove", (event) => {
        mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
        mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;
    });

    window.addEventListener("keydown", function onPress(event) {
        if (event.key === "Shift") {
            shiftPressed = true;
        }
    });
    
    window.addEventListener("keyup", function onRelease(event) {
        if (event.key === "Shift") {
            shiftPressed = false;
        }
    });

    window.addEventListener("click", () => {
        raycaster.setFromCamera(mouse, camera);
        const intersects = raycaster.intersectObjects(rubikCube.arrows, true);
        if (intersects.length > 0) {
            let intersectedObject = intersects[0].object.parent?.name;
            if(intersectedObject) {
                if(shiftPressed) intersectedObject = intersectedObject + "'";
                rubikCube.applyMoves(intersectedObject);
            }
        }
    });

    for(let arrow of rubikCube.arrows) {
        raycasteable.push(arrow);
    }

    raycasteable.push(rubikCube.getCube());
}

function update() {
    requestAnimationFrame(update);

    // stats.update();

    if (resizeRendererToDisplaySize(renderer)) {
        const canvas = renderer.domElement;
        camera.aspect = canvas.clientWidth / canvas.clientHeight;
        camera.updateProjectionMatrix();
    }

    raycaster.setFromCamera(mouse, camera);
    const intersects = raycaster.intersectObjects(rubikCube.arrows, true);
    if (intersects.length > 0) {
        document.body.style.cursor = 'pointer';
    } else {
        document.body.style.cursor = 'auto';
    }
    renderer.render(scene, camera);

    cameraControls.update();
    

    renderer.render(scene, camera);
}

export function setSteps(a: any){
    stepList = a;
}
