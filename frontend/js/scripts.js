document.addEventListener("DOMContentLoaded", () => {
    const tree = document.getElementById("tree");
    const treeContainer = document.getElementById("tree-container");
    const form = document.getElementById("letter-form");
    const snowContainer = document.getElementById("snow");

    const modal = document.getElementById("modal");
    const modalMessage = document.getElementById("modal-message");
    const modalAuthor = document.getElementById("modal-author");
    const closeModal = document.getElementById("close-modal");

    // 모달 열기
    const showModal = (message, author) => {
        modalMessage.textContent = `Message: ${message}`;
        modalAuthor.textContent = `Written by: ${author}`;
        modal.style.display = "block";
    };

    // 모달 닫기
    closeModal.addEventListener("click", () => {
        modal.style.display = "none";
    });

    // 트리 내부에서 가장자리 제외한 랜덤 위치 생성
    const getRandomPositionWithinTree = () => {
        const treeBounds = tree.getBoundingClientRect();

        let x, y;
        let insideTree = false;

        while (!insideTree) {
            // 랜덤 x, y 위치 계산
            x = Math.random() * treeBounds.width;
            y = Math.random() * treeBounds.height;

            const relativeX = x / treeBounds.width;
            const relativeY = y / treeBounds.height;

            // 가장자리를 제외한 삼각형 영역 내 확인
            const margin = 0.4; // 가장자리 제외 범위 (10%)
            if (
                relativeY >= relativeX - margin && // 왼쪽 가장자리 제외
                relativeY >= 1 - relativeX - margin && // 오른쪽 가장자리 제외
                relativeY <= 1 - margin // 상단 여백 제외
            ) {
                insideTree = true;
            }
        }

        return { x, y };
    };

    // 오너먼트 추가 함수
    const addOrnament = (username, message, author) => {
        const ornament = document.createElement("div");
        ornament.className = "ornament";

        // 위치 설정
        const { x, y } = getRandomPositionWithinTree();
        ornament.style.left = `${x}px`;
        ornament.style.top = `${y}px`;

        // 클릭 이벤트로 모달 열기
        ornament.addEventListener("click", (e) => {
            e.stopPropagation(); // 클릭 이벤트가 트리로 전달되지 않도록 방지
            showModal(message, author); // 작성자(author)를 전달
        });

        treeContainer.appendChild(ornament);
    };

    // 폼 제출 이벤트
    form.addEventListener("submit", (e) => {
        e.preventDefault();

        const username = document.getElementById("recipient-username").value.trim();
        const message = document.getElementById("letter-content").value.trim();
        const author = document.getElementById("author-name").value.trim();

        if (username && message && author) {
            addOrnament(username, message, author); // 작성자(author)를 전달
            form.reset();
            alert("Your message has been added as an ornament!");
        } else {
            alert("Please fill in all fields.");
        }
    });

    // 트리 클릭 방지
    tree.addEventListener("click", (e) => {
        e.stopPropagation(); // 트리 클릭 이벤트 무시
    });

    // 눈 결정 생성 함수
    const createSnowflake = () => {
        const snowflake = document.createElement("div");
        snowflake.className = "snowflake";

        // 랜덤 위치와 속성 설정
        snowflake.style.left = Math.random() * window.innerWidth + "px";
        snowflake.style.animationDuration = Math.random() * 5 + 5 + "s";
        snowflake.style.opacity = Math.random() * 0.5 + 0.3;
        snowflake.style.width = snowflake.style.height = Math.random() * 8 + 4 + "px";

        snowContainer.appendChild(snowflake);

        // 눈 결정이 화면 밖으로 사라지면 삭제
        snowflake.addEventListener("animationend", () => {
            snowflake.remove();
        });
    };

    // 일정 간격으로 눈 생성
    setInterval(createSnowflake, 150);
});

document.addEventListener("DOMContentLoaded", () => {
    const createTreeButton = document.getElementById("create-tree-button");
    const signupModal = document.getElementById("signup-modal");
    const closeSignupModal = document.getElementById("close-signup-modal");
    const signupForm = document.getElementById("signup-form");

    // Create Tree 버튼 클릭 시 모달 열기
    createTreeButton.addEventListener("click", () => {
        signupModal.style.display = "flex";
    });

    // 모달 닫기
    closeSignupModal.addEventListener("click", () => {
        signupModal.style.display = "none";
    });

    // 폼 제출 이벤트
    signupForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const username = document.getElementById("username").value.trim();
        const password = document.getElementById("password").value.trim();

        if (username && password) {
            try {
                // 서버와 통신 (백엔드 연동)
                const response = await fetch("/create-tree", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ username, password }),
                });

                if (response.ok) {
                    const result = await response.json();
                    alert(result.message || "Tree created successfully!");
                    signupModal.style.display = "none"; // 모달 닫기
                } else {
                    alert("Failed to create tree. Try again.");
                }
            } catch (error) {
                console.error("Error:", error);
                alert("An error occurred while creating the tree.");
            }
        } else {
            alert("Please fill in all fields.");
        }
    });

    // 모달 외부 클릭 시 닫기
    window.addEventListener("click", (e) => {
        if (e.target === signupModal) {
            signupModal.style.display = "none";
        }
    });
});
