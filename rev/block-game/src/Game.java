import javax.swing.JFrame;
import java.awt.Color;
import java.awt.image.BufferStrategy;
import java.nio.ByteBuffer;
import java.awt.Graphics2D;

public class Game extends JFrame implements Runnable {

    private boolean running = false;

    public static final int FPS = 60;
    private static final double deltaBetweenFrames = 1000000000D / FPS;

    public static final int TILE_SIZE = 20;

    public static final int MAX_Z = 8;

    private final Tile[][][] tiles;

    private final Player player;
    private final Inventory inventory;
    private final int mapWidth, mapHeight;

    public Game(int mapWidth, int mapHeight) {
        this.mapWidth = mapWidth;
        this.mapHeight = mapHeight;

        this.tiles = new Tile[mapHeight][mapWidth][MAX_Z];

        for (int y = 0; y < tiles.length; y++) {
            for (int x = 0; x < tiles[y].length; x++) {
                for (int z = 0; z < tiles[y][x].length; z++) {
                    if (z == MAX_Z - 1) {
                        tiles[y][x][z] = new Tile(Tile.TileType.GRASS, x, y, z);

                        if (Math.random() < 0.04) {
                            tiles[y][x][z].setType(Tile.TileType.WATER);
                        } else if (Math.random() < 0.2) {
                            tiles[y][x][z].setType(Tile.TileType.SAND);
                        }
                    } else if (z >= 4) {
                        tiles[y][x][z] = new Tile(Tile.TileType.DIRT, x, y, z);

                        if (Math.random() > z / 10D) {
                            tiles[y][x][z].setType(Tile.TileType.STONE);
                        }
                    } else {
                        tiles[y][x][z] = new Tile(Tile.TileType.STONE, x, y, z);

                        if (Math.random() < 0.2) {
                            tiles[y][x][z].setType(Tile.TileType.GRANITE);
                        } else if (Math.random() < 0.008) {
                            tiles[y][x][z].setType(Tile.TileType.LAVA);
                        } else if (Math.random() < 0.005) {
                            tiles[y][x][z].setType(Tile.TileType.IRON);
                        } else if (Math.random() < 0.004) {
                            tiles[y][x][z].setType(Tile.TileType.LAPIS);
                        } else if (Math.random() < 0.003) {
                            tiles[y][x][z].setType(Tile.TileType.GOLD);
                        } else if (Math.random() < 0.002) {
                            tiles[y][x][z].setType(Tile.TileType.DIAMOND);
                        } else if (Math.random() < 0.001) {
                            tiles[y][x][z].setType(Tile.TileType.EMERALD);
                        }
                    }

                    if (Math.random() < 0.0001) {
                        tiles[y][x][z].setType(Tile.TileType.STAIRS_DOWN);
                    } else if (Math.random() < 0.0001) {
                        tiles[y][x][z].setType(Tile.TileType.STAIRS_UP);
                    }
                }
            }
        }

        inventory = new Inventory(this);
        player = new Player(this, inventory, tiles[0].length / 2, tiles.length / 2, 0);
    }

    public void saveData() {
        int gen = 0;
        byte[] data = new byte[17 + tiles.length * tiles[0].length * 4];

        for (byte b : ByteBuffer.allocate(4).putInt((int) player.getX()).array()) {
            System.out.println(b);
            data[gen++] = b;
        }

        for (byte b : ByteBuffer.allocate(4).putInt((int) player.getY()).array()) {
            data[gen++] = b;
        }

        data[gen++] = (byte) player.getZ();

        for (byte b : ByteBuffer.allocate(4).putInt(mapWidth).array()) {
            data[gen++] = b;
        }

        for (byte b : ByteBuffer.allocate(4).putInt(mapHeight).array()) {
            data[gen++] = b;
        }

        for (int y = 0; y < tiles.length; y++) {
            for (int x = 0; x < tiles[y].length; x++) {
                for (int zz = 0; zz < MAX_Z; zz += 2) {
                    byte enc = 0;
                    for (int z = 0; z < 2; z++) {
                        enc |= (byte) (tiles[y][x][z + zz].getType().id << (z * 4));
                    }
                    data[gen++] = enc;
                }
            }
        }

        FileManager.saveData(data);
    }

    public Tile getTileAt(int x, int y, int z) {
        if (x < 0 || y < 0 || z < 0 || y >= tiles.length || x >= tiles[0].length || z >= tiles[0][0].length) {
            return null;
        }

        return tiles[y][x][z];
    }

    public void tick() {
        player.tick();
    }

    public static final Color BACKGROUND_COLOR = new Color(0x99eaff);

    public void render() {
        BufferStrategy bs = this.getBufferStrategy();
        if (bs == null) {
            this.createBufferStrategy(3);
            return;
        }

        Graphics2D g = (Graphics2D) bs.getDrawGraphics();

        g.setColor(BACKGROUND_COLOR);
        g.fillRect(0, 0, getWidth(), getHeight());

        double playerOffsetX = player.getX() * TILE_SIZE - getWidth() / 2;
        double playerOffsetY = player.getY() * TILE_SIZE - getHeight() / 2;

        for (int y = Math.max(0, (int) player.getY() - getHeight() / TILE_SIZE); y < Math.min(tiles.length,
                player.getY() + getHeight() / TILE_SIZE); y++) {
            for (int x = Math.max(0, (int) player.getX() - getWidth() / TILE_SIZE); x < Math.min(tiles[0].length,
                    player.getX()
                            + getWidth() / TILE_SIZE); x++) {
                Tile t = tiles[y][x][player.getZ()];
                t.render(g, playerOffsetX, playerOffsetY);
            }
        }

        player.render(g, getWidth() / 2, getHeight() / 2);
        inventory.render(g);

        g.dispose();

        bs.show();
    }

    public int getMapWidth() {
        return mapWidth;
    }

    public int getMapHeight() {
        return mapHeight;
    }

    public Player getPlayer() {
        return player;
    }

    public synchronized void start() {
        if (this.running)
            return;
        this.running = true;
        new Thread(this).start();
    }

    public synchronized void stop() {
        if (!this.running)
            return;
        try {
            Thread.currentThread().join();
            this.running = false;
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    @Override
    public void run() {
        int frames = 0;

        double lastTime = System.nanoTime();
        double lastTimer = System.currentTimeMillis();
        double currentTime, currentTimer;
        while (running) {
            currentTime = System.nanoTime();
            if (currentTime - lastTime >= deltaBetweenFrames) {
                tick();
                render();
                lastTime = currentTime;
                frames++;
            }

            currentTimer = System.currentTimeMillis();
            if (currentTimer - lastTimer >= 1000) {
                System.out.println("FPS: " + frames);
                frames = 0;
                lastTimer = currentTimer;
            }
        }
    }
}
