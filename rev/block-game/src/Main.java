import javax.swing.JFrame;

public class Main {
    public static void main(String[] args) {
        Game game = new Game(500, 500);
        game.setTitle("Block Game");
        game.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        game.setSize(800, 800);

        game.setVisible(true);

        game.start();
    }
}
