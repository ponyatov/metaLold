package io.github.ponyatov.metal;

public class Frame {

    /// type/class tag
    final static String type = "frame";

    /// object value (primitive implementation language type)
    String value;

    /// construct new frame/object with given name
    public Frame(String V) {
        value = V;
    }

    /// dump in short form: header only
    public String head(String prefix) {
        return prefix + "<" + type + ":" + value + ">";
    }
    public String head() { return head(""); }

    public String dump(int depth, String prefix) {
        String S = pad(depth) + head(prefix);
        return S;
    }
    public String dump(int depth)   { return dump(depth,"");    }
    public String dump()            { return dump(0,""); }

    String pad(int N) {
        final String cr  = "\n";
        final String tab = "\t";
        String S = cr;
        for (int i=0;i<N;i++) S += tab;
        return S;
    }

}
