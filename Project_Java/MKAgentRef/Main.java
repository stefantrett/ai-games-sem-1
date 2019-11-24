// 
// Decompiled by Procyon v0.5.36
// 

package MKAgentRef;

import MKAgent.InvalidMessageException;
import java.io.IOException;
import java.io.EOFException;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.Reader;

public class Main
{
    private static final int holes = 7;
    private static final int seeds = 7;
    private static Reader input;
    
    static {
        Main.input = new BufferedReader(new InputStreamReader(System.in));
    }
    
    public static void sendMsg(final String msg) {
        System.out.print(msg);
        System.out.flush();
    }
    
    public static String recvMsg() throws IOException {
        final StringBuilder message = new StringBuilder();
        int newCharacter;
        do {
            newCharacter = Main.input.read();
            if (newCharacter == -1) {
                throw new EOFException("Input ended unexpectedly.");
            }
            message.append((char)newCharacter);
        } while ((char)newCharacter != '\n');
        return message.toString();
    }
    
    public static void main(final String[] args) {
        try {
            new Agent(7, 7).play();
        }
        catch (IOException e) {
            System.err.println("Communication error: " + e.getMessage());
        }
        catch (InvalidMessageException e2) {
            System.err.println("THIS IS A REAL BUG: " + e2.getMessage());
        }
    }
}
