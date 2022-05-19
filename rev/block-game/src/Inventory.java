import java.awt.Color;
import java.awt.Graphics;
import java.util.ArrayList;
import java.util.List;

public class Inventory {
    private final int height = 50;
    private final int width;

    private final Game game;

    private final InventoryItem[] items;

    private int selectedItem = 0;

    public Inventory(Game game) {
        this.game = game;

        List<InventoryItem> items = new ArrayList<>();
        for (int i = 0; i < Tile.TileType.values().length; i++) {
            if (!Tile.TileType.values()[i].showInInventory)
                continue;

            items.add(new InventoryItem(Tile.TileType.values()[i]));
        }
        this.items = items.toArray(new InventoryItem[0]);

        this.width = this.items.length * (height - 10) + 10;
    }

    public void tick() {
    }

    private final Color backgroundColor = new Color(255, 255, 255, 70);

    public void render(Graphics g) {
        g.setColor(backgroundColor);
        g.fillRect(game.getWidth() / 2 - width / 2, game.getHeight() - height * 2, width, height);
        int xOffset = 0;
        for (InventoryItem item : items) {
            if (selectedItem == xOffset) {
                g.setColor(backgroundColor);
                g.fillRect(game.getWidth() / 2 - width / 2 + (height - 10) * xOffset + 5,
                        game.getHeight() - height * 2 + 5, height - 10, height - 10);
            }

            g.setColor(item.type.color);
            g.fillRect(game.getWidth() / 2 - width / 2 + (height - 10) * xOffset + 10,
                    game.getHeight() - height * 2 + 10, height - 20,
                    height - 20);
            xOffset++;
        }
    }

    public InventoryItem getSelectedItem() {
        return items[selectedItem];
    }

    public void setSelectedItem(int selectedItem) {
        while (selectedItem < 0) {
            selectedItem += items.length;
        }

        this.selectedItem = selectedItem % items.length;
    }

    class InventoryItem {
        private final Tile.TileType type;

        public InventoryItem(Tile.TileType type) {
            this.type = type;
        }

        public Tile.TileType getType() {
            return type;
        }
    }
}
