import java.awt.Color;
import java.awt.Graphics;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.awt.event.MouseEvent;
import java.awt.event.MouseWheelEvent;
import java.awt.event.MouseListener;
import java.awt.event.MouseWheelListener;
import java.util.HashMap;
import java.util.Map;

public class Player implements KeyListener, MouseListener, MouseWheelListener {

    Map<Integer, Boolean> keys = new HashMap<Integer, Boolean>();

    private Game game;
    private Inventory inventory;

    private double x = 0, y = 0;
    private int z = 0;

    private boolean onStairs = false;

    public Player(Game game, Inventory inventory, int x, int y, int z) {
        this.game = game;

        this.x = x;
        this.y = y;
        this.z = z;

        this.inventory = inventory;

        game.addKeyListener(this);
        game.addMouseListener(this);
        game.addMouseWheelListener(this);
    }

    @Override
    public void keyTyped(KeyEvent e) {

    }

    @Override
    public void keyPressed(KeyEvent e) {
        keys.put(e.getKeyCode(), true);

        if (e.getKeyCode() == KeyEvent.VK_ESCAPE) {
            System.exit(0);
        } else if (e.getKeyCode() == KeyEvent.VK_P) {
            game.saveData();
        }
    }

    @Override
    public void keyReleased(KeyEvent e) {
        keys.put(e.getKeyCode(), false);
    }

    public void tick() {
        if (keys.getOrDefault(KeyEvent.VK_W, false)) {
            y -= 0.1;
        }

        if (keys.getOrDefault(KeyEvent.VK_S, false)) {
            y += 0.1;
        }

        if (keys.getOrDefault(KeyEvent.VK_A, false)) {
            x -= 0.1;
        }

        if (keys.getOrDefault(KeyEvent.VK_D, false)) {
            x += 0.1;
        }

        x = Math.max(0.5, Math.min(x, game.getMapWidth() - 0.5));
        y = Math.max(0.5, Math.min(y, game.getMapHeight() - 0.5));

        Tile currTile = game.getTileAt((int) x, (int) y, z);

        if (currTile.getType() == Tile.TileType.STAIRS_DOWN) {
            if (!onStairs && z > 0) {
                z--;
            }
            onStairs = true;
        } else if (currTile.getType() == Tile.TileType.STAIRS_UP) {
            if (!onStairs && z < Game.MAX_Z - 1) {
                z++;
            }
            onStairs = true;
        } else {
            onStairs = false;
        }
    }

    public void build(int x, int y) {
        if (inActionRange(x, y)) {
            Inventory.InventoryItem item = inventory.getSelectedItem();
            game.getTileAt(x, y, this.z).setType(item.getType());
        }
    }

    public void destroy(int x, int y) {
        if (inActionRange(x, y)) {
            game.getTileAt(x, y, this.z).setType(Tile.TileType.EMPTY);
        }
    }

    public boolean inActionRange(int x, int y) {
        return Math.pow(x - this.x, 2) + Math.pow(y - this.y, 2) < 25;
    }

    public void render(Graphics g, int locX, int locY) {
        g.setColor(Color.RED);

        g.fillRect(locX - Game.TILE_SIZE / 2, locY - Game.TILE_SIZE / 2, Game.TILE_SIZE,
                Game.TILE_SIZE);
    }

    public double getX() {
        return x;
    }

    public double getY() {
        return y;
    }

    public int getZ() {
        return z;
    }

    public void setX(double x) {
        this.x = x;
    }

    public void setY(double y) {
        this.y = y;
    }

    public void setZ(int z) {
        if (z < 0 || z > Game.MAX_Z) {
            return;
        }
        this.z = z;
    }

    @Override
    public void mouseClicked(MouseEvent e) {
    }

    @Override
    public void mousePressed(MouseEvent e) {
        int x = (int) ((e.getX() + getX() * Game.TILE_SIZE - game.getWidth() / 2) / Game.TILE_SIZE);
        int y = (int) ((e.getY() + getY() * Game.TILE_SIZE - game.getHeight() / 2) / Game.TILE_SIZE);
        if (e.getButton() == MouseEvent.BUTTON3) {
            build(x, y);
        } else if (e.getButton() == MouseEvent.BUTTON1) {
            destroy(x, y);
        }
    }

    @Override
    public void mouseReleased(MouseEvent e) {
    }

    @Override
    public void mouseWheelMoved(MouseWheelEvent e) {
        inventory
                .setSelectedItem(inventory.getSelectedItem().getType().id + e.getScrollAmount() / e.getUnitsToScroll());
    }

    @Override
    public void mouseEntered(MouseEvent e) {
    }

    @Override
    public void mouseExited(MouseEvent e) {
    }
}
