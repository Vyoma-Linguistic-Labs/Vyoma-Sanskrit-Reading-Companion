<!-- JavaScript for Side Drawer Menu -->
        // Function to open the side drawer
    function openNav() {
        document.getElementById('side-drawer').style.width = "250px";
        document.addEventListener('click', closeOnClickOutside); // Add the event listener when the menu opens
    }

    // Function to close the side drawer
    function closeNav() {
        document.getElementById('side-drawer').style.width = "0";
        document.removeEventListener('click', closeOnClickOutside); // Remove the event listener when the menu closes
    }

        // Close the menu when clicking outside of it
    function closeOnClickOutside(event) {
        const drawer = document.getElementById('side-drawer');
        const menuButton = document.getElementById('menu-button'); // Ensure clicking the button itself doesn't close the menu
        if (!drawer.contains(event.target) && !menuButton.contains(event.target)) {
            closeNav(); // Close the drawer if clicked outside
        }
    }

        // Fetch menu.csv data dynamically from the server
        const menuItems = {{ menu_items | tojson }};
        const menuList = document.getElementById('menu-list');

        // Populate the side drawer menu
        menuItems.forEach(item => {
            const mainMenuItem = document.createElement('li');
            mainMenuItem.textContent = item['Main Menu'];

            const subMenuList = document.createElement('ul'); // Sub-menu for second level

            const subMenuArray = item['Sub Menu'].split(';');
            const subMenuLinksArray = item['Sub Menu Link'].split(';');

            subMenuArray.forEach((subItem, index) => {
                const subMenuItem = document.createElement('li');
                const subMenuLink = document.createElement('a');
                subMenuLink.href = subMenuLinksArray[index]; // Link to the submenu
                subMenuLink.textContent = subItem;

                subMenuItem.appendChild(subMenuLink);
                subMenuList.appendChild(subMenuItem);
            });

            mainMenuItem.appendChild(subMenuList); // Add sub-menu to main menu item
            menuList.appendChild(mainMenuItem); // Add main menu item to the list
        });

        // Sub-menu visibility on hover
        const allMainMenuItems = document.querySelectorAll("#menu-list > li");
        allMainMenuItems.forEach(mainMenu => {
            mainMenu.onmouseover = function() {
                mainMenu.querySelector("ul").style.display = "block";
            };
            mainMenu.onmouseout = function() {
                mainMenu.querySelector("ul").style.display = "none";
            };
        });
