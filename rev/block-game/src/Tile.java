import java.awt.Color;
import java.awt.Graphics;

public class Tile {
    private int x, y, z;
    private TileType type;

    public Tile(TileType type, int x, int y, int z) {
        this.type = type;
        this.x = x;
        this.y = y;
        this.z = z;
    }

    public int getX() {
        return x;
    }

    public int getY() {
        return y;
    }

    public int getZ() {
        return z;
    }

    public TileType getType() {
        return type;
    }

    public void setType(TileType type) {
        this.type = type;
    }

    public void render(Graphics g, double playerX, double playerY) {
        g.setColor(type.color);
        g.fillRect((int) Math.round(x * Game.TILE_SIZE - playerX), (int) Math.round(y * Game.TILE_SIZE - playerY),
                Game.TILE_SIZE, Game.TILE_SIZE);
    }

    public enum TileType {
        STONE(0, "Stone", new Color(0x888c8d), true),
        GRANITE(1, "Granite", new Color(0xcd8032), true),
        SAND(2, "Sand", new Color(0xdbb17a), true),
        DIRT(3, "Dirt", new Color(0xb37a4c), true),
        GRASS(4, "Grass", new Color(0x009a17), true),
        WOOD(5, "Wood", new Color(0xca9c67), true),
        IRON(6, "Iron", new Color(0xcfcfcf), true),
        GOLD(7, "Gold", new Color(0xfccd12), true),
        LAPIS(8, "Lapis", new Color(0x00b2ff), true),
        DIAMOND(9, "Diamond", new Color(0xb9f2ff), true),
        EMERALD(10, "Emerald", new Color(0x3aab58), true),
        WATER(11, "Water", new Color(0x337cba), true),
        LAVA(12, "Lava", new Color(0xf83a0c), true),
        STAIRS_DOWN(13, "StairsD", Color.BLACK, true),
        STAIRS_UP(14, "StairsU", Color.WHITE, true),
        EMPTY(15, "Empty", Game.BACKGROUND_COLOR, false);

        public final int id;
        public final String name;
        public final Color color;
        public final boolean showInInventory;

        TileType(int id, String name, Color color, boolean showInInventory) {
            this.id = id;
            this.name = name;
            this.color = color;
            this.showInInventory = showInInventory;
        }
    }
}
