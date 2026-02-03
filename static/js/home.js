document.addEventListener("DOMContentLoaded", () => {
    // --- HERO SLIDER LOGIC ---
    const slides = document.querySelectorAll(".hero-slide");
    const dots = document.querySelectorAll(".hero-dot");
    let currentSlide = 0;

    function showSlide(index) {
        slides.forEach((slide, i) => {
            const content = slide.querySelector(".slide-content");
            if (i === index) {
                slide.classList.remove("opacity-0", "z-0");
                slide.classList.add("opacity-100", "z-10");
                // Text animation
                content.classList.remove("translate-y-4", "opacity-0");
                content.classList.add("translate-y-0", "opacity-100");
                // Dot styling
                dots[i].classList.remove("bg-white/20", "w-1.5");
                dots[i].classList.add("bg-xiaomi", "w-6");
            } else {
                slide.classList.remove("opacity-100", "z-10");
                slide.classList.add("opacity-0", "z-0");
                content.classList.remove("translate-y-0", "opacity-100");
                content.classList.add("translate-y-4", "opacity-0");
                dots[i].classList.remove("bg-xiaomi", "w-6");
                dots[i].classList.add("bg-white/20", "w-1.5");
            }
        });
        currentSlide = index;
    }

    // Auto play
    setInterval(() => {
        let next = (currentSlide + 1) % slides.length;
        showSlide(next);
    }, 5000);

    // Dot clicks
    dots.forEach((dot) => {
        dot.addEventListener("click", () => {
            showSlide(parseInt(dot.dataset.index));
        });
    });

    // --- TABS LOGIC ---
    const tabServices = document.getElementById("tab-services");
    const tabProducts = document.getElementById("tab-products");
    const contentServices = document.getElementById("content-services");
    const contentProducts = document.getElementById("content-products");

    function switchTab(tabName) {
        if (tabName === "services") {
            tabServices.classList.add(
                "bg-primary",
                "dark:bg-white",
                "text-white",
                "dark:text-black",
                "shadow-md"
            );
            tabServices.classList.remove("text-gray-500", "hover:bg-gray-50");

            tabProducts.classList.remove(
                "bg-primary",
                "dark:bg-white",
                "text-white",
                "dark:text-black",
                "shadow-md"
            );
            tabProducts.classList.add("text-gray-500", "dark:text-gray-400");

            contentServices.classList.remove("hidden");
            contentProducts.classList.add("hidden");
        } else {
            tabProducts.classList.add(
                "bg-primary",
                "dark:bg-white",
                "text-white",
                "dark:text-black",
                "shadow-md"
            );
            tabProducts.classList.remove("text-gray-500");

            tabServices.classList.remove(
                "bg-primary",
                "dark:bg-white",
                "text-white",
                "dark:text-black",
                "shadow-md"
            );
            tabServices.classList.add("text-gray-500", "dark:text-gray-400");

            contentProducts.classList.remove("hidden");
            contentServices.classList.add("hidden");
        }
    }

    tabServices.addEventListener("click", () => switchTab("services"));
    tabProducts.addEventListener("click", () => switchTab("products"));

    // --- WISHLIST LOGIC (Visual Only) ---
    const wishBtns = document.querySelectorAll(".wishlist-btn");
    wishBtns.forEach((btn) => {
        btn.addEventListener("click", function (e) {
            e.stopPropagation(); // prevent triggering card click
            const icon = this.querySelector(".material-icons");
            if (icon.textContent === "favorite_border") {
                icon.textContent = "favorite";
                this.classList.add("text-red-500");
                this.classList.remove("text-gray-400");
            } else {
                icon.textContent = "favorite_border";
                this.classList.remove("text-red-500");
                this.classList.add("text-gray-400");
            }
        });
    });

    // --- TESTIMONIALS LOGIC ---
    const defaultTestimonials = [
        {
            text: "La rapidez con la que liberaron mi iPhone 14 Pro fue impresionante. En 20 minutos ya tenía señal.",
            author: "Marcela V.",
            image: "https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&q=80&w=150",
        },
        {
            text: "Pensé que mi pantalla curva no tenía solución barata. Quedó original y mantuve mis 120Hz.",
            author: "Jorge L.",
            image: "https://images.unsplash.com/photo-1599566150163-29194dcaad36?auto=format&fit=crop&q=80&w=150",
        },
    ];

    const testimonials = (window.TESTIMONIALS_DATA && window.TESTIMONIALS_DATA.length > 0) 
        ? window.TESTIMONIALS_DATA 
        : defaultTestimonials;
    let currentTestim = 0;
    const testimImg = document.getElementById("testim-img");
    const testimAuthor = document.getElementById("testim-author");
    const testimText = document.getElementById("testim-text");

    function updateTestimonial(idx) {
        // Simple fade effect simulation could be added here
        const data = testimonials[idx];
        testimImg.src = data.image;
        testimAuthor.textContent = data.author;
        testimText.textContent = `"${data.text}"`;
    }

    document.getElementById("next-testim").addEventListener("click", () => {
        currentTestim = (currentTestim + 1) % testimonials.length;
        updateTestimonial(currentTestim);
    });
    document.getElementById("prev-testim").addEventListener("click", () => {
        currentTestim =
            (currentTestim - 1 + testimonials.length) % testimonials.length;
        updateTestimonial(currentTestim);
    });
});

// --- BENTO GRID INTERACTION ---
const bLargImg = document.getElementById("bento-large-img-current");
const bLargTitle = document.getElementById("bento-large-title");
const bLargDesc = document.getElementById("bento-large-desc");
const bSmallCards = document.querySelectorAll(".bento-small-card");

if (bLargImg && bSmallCards.length > 0) {
    bSmallCards.forEach((card) => {
        card.addEventListener("click", () => {
            // 1. Capture Current Large State
            const oldLargeImg = bLargImg.src;
            const oldLargeTitle = bLargTitle.innerText; // Use innerText for safety
            const oldLargeDesc = bLargDesc.innerText;

            // 2. Capture Clicked Small State (from dataset)
            const newLargeImg = card.dataset.img;
            const newLargeTitle = card.dataset.title;
            const newLargeDesc = card.dataset.desc;

            // 3. Update Large Card (with simple fade effect manually handled or direct swap)
            // Direct swap for instant responsiveness as requested
            bLargImg.src = newLargeImg;
            bLargTitle.textContent = newLargeTitle;
            bLargDesc.textContent = newLargeDesc;

            // 4. Update Small Card (Swap content to where it came from)
            // Update dataset for next click
            card.dataset.img = oldLargeImg;
            card.dataset.title = oldLargeTitle;
            card.dataset.desc = oldLargeDesc;

            // Update DOM elements of the small card
            const smallImg = card.querySelector("img");
            const smallTitle = card.querySelector("h4");

            if (smallImg) smallImg.src = oldLargeImg;
            if (smallTitle) smallTitle.textContent = oldLargeTitle;
        });
    });
}
